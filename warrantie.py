
import sqlite3
from datetime import date, timedelta
from contextlib import contextmanager


DB_NAME = "warrantie.db"


@contextmanager
def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        yield conn
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def initialize_database():

    with connect_db() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL UNIQUE,
                email TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                purchase_id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                receipt_no TEXT NOT NULL UNIQUE,
                purchase_date TEXT NOT NULL,
                warranty_days INTEGER NOT NULL,
                expiration_date TEXT NOT NULL,
                FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS claims (
                claim_id INTEGER PRIMARY KEY,
                purchase_id INTEGER NOT NULL,
                issue TEXT NOT NULL,
                claim_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                resolution_type TEXT,
                resolution_notes TEXT,
                FOREIGN KEY (purchase_id)
                    REFERENCES purchases(purchase_id)
            )
        """)


def get_required_input(message):

    while True:
        value = input(message).strip()

        if value:
            return value

        print("Error: This field cannot be empty.")


def get_valid_date(message):

    while True:
        try:
            entered_date = input(message).strip()
            parsed_date = date.fromisoformat(entered_date)

            if parsed_date > date.today():
                print("Error: Purchase date cannot be in the future.")
                continue

            return parsed_date

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD format.")


def get_positive_integer(message):

    while True:
        try:
            number = int(input(message))

            if number <= 0:
                print("Error: Enter a number greater than zero.")
                continue

            return number

        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_claim_id():

    while True:
        try:
            return int(input("Enter Claim ID: "))

        except ValueError:
            print("Invalid Claim ID. Please enter a number.")


def register_purchase():

    print("\n========== REGISTER NEW PURCHASE ==========")

    name = get_required_input("Customer Name: ")
    phone = get_required_input("Contact Number: ")
    email = input("Email Address (optional): ").strip()

    product_name = get_required_input("Product Name: ")
    brand = get_required_input("Brand: ")
    model = get_required_input("Model: ")

    receipt_no = get_required_input("Receipt Number: ")

    purchase_date = get_valid_date(
        "Purchase Date (YYYY-MM-DD): "
    )

    warranty_days = get_positive_integer(
        "Warranty Duration (days): "
    )

    expiration_date = purchase_date + timedelta(
        days=warranty_days
    )

    try:

        with connect_db() as conn:

            
            customer = conn.execute("""
                SELECT customer_id
                FROM customers
                WHERE phone = ?
            """, (phone,)).fetchone()

            if customer:
                customer_id = customer["customer_id"]

                print("\nExisting customer found.")

            else:
                cursor = conn.execute("""
                    INSERT INTO customers
                    (name, phone, email)
                    VALUES (?, ?, ?)
                """, (name, phone, email))

                customer_id = cursor.lastrowid

           
            conn.execute("""
                INSERT INTO purchases (
                    customer_id,
                    product_name,
                    brand,
                    model,
                    receipt_no,
                    purchase_date,
                    warranty_days,
                    expiration_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                customer_id,
                product_name,
                brand,
                model,
                receipt_no,
                purchase_date.isoformat(),
                warranty_days,
                expiration_date.isoformat()
            ))

        print("\nPurchase successfully registered!")
        print("Customer:", name)
        print("Product:", product_name)
        print("Receipt Number:", receipt_no)
        print("Warranty Expires:", expiration_date)

    except sqlite3.IntegrityError:
        print("\nError: Receipt number or customer information already exists.")

    except sqlite3.Error as error:
        print("\nDatabase Error:", error)


def search_purchase():

    print("\n========== SEARCH PURCHASE ==========")

    receipt_no = get_required_input("Enter Receipt Number: ")

    try:

        with connect_db() as conn:

            purchase = conn.execute("""
                SELECT
                    p.*,
                    c.name,
                    c.phone,
                    c.email
                FROM purchases p
                JOIN customers c
                    ON p.customer_id = c.customer_id
                WHERE p.receipt_no = ?
            """, (receipt_no,)).fetchone()

        if purchase is None:
            print("\nNo purchase record found.")
            return

        print("\n========== PURCHASE DETAILS ==========")

        print("Customer ID:", purchase["customer_id"])
        print("Customer Name:", purchase["name"])
        print("Contact Number:", purchase["phone"])
        print("Email:", purchase["email"])

        print("\nProduct:", purchase["product_name"])
        print("Brand:", purchase["brand"])
        print("Model:", purchase["model"])

        print("Receipt Number:", purchase["receipt_no"])
        print("Purchase Date:", purchase["purchase_date"])

        print("Warranty Duration:",
              purchase["warranty_days"], "days")

        print("Expiration Date:",
              purchase["expiration_date"])

        today = date.today()
        expiration = date.fromisoformat(
            purchase["expiration_date"]
        )

        if today <= expiration:
            print("Warranty Status: ACTIVE")
        else:
            print("Warranty Status: EXPIRED")

    except sqlite3.Error as error:
        print("\nDatabase Error:", error)


def submit_claim():

    print("\n========== SUBMIT WARRANTY CLAIM ==========")

    receipt_no = get_required_input("Enter Receipt Number: ")

    try:

        with connect_db() as conn:

            purchase = conn.execute("""
                SELECT *
                FROM purchases
                WHERE receipt_no = ?
            """, (receipt_no,)).fetchone()

            if purchase is None:
                print("\nError: Purchase record not found.")
                return

            today = date.today()

            expiration = date.fromisoformat(
                purchase["expiration_date"]
            )

            if today > expiration:
                print("\nClaim rejected: Warranty has expired.")
                return

            print("\nProduct:", purchase["product_name"])
            print("Warranty Status: ACTIVE")

            issue = get_required_input(
                "Describe the Product Issue: "
            )

            conn.execute("""
                INSERT INTO claims (
                    purchase_id,
                    issue,
                    claim_date,
                    status
                )
                VALUES (?, ?, ?, 'Pending')
            """, (
                purchase["purchase_id"],
                issue,
                today.isoformat()
            ))

        print("\nWarranty claim successfully submitted!")
        print("Status: Pending")

    except sqlite3.Error as error:
        print("\nDatabase Error:", error)


def view_claims():

    print("\n========== ALL WARRANTY CLAIMS ==========")

    try:

        with connect_db() as conn:

            claims = conn.execute("""
                SELECT
                    cl.claim_id,
                    cl.issue,
                    cl.claim_date,
                    cl.status,
                    cl.resolution_type,
                    p.product_name,
                    p.receipt_no,
                    c.name
                FROM claims cl
                JOIN purchases p
                    ON cl.purchase_id = p.purchase_id
                JOIN customers c
                    ON p.customer_id = c.customer_id
                ORDER BY cl.claim_id
            """).fetchall()

        if not claims:
            print("\nNo warranty claims recorded.")
            return

        for claim in claims:

            print("\n----------------------------------------")
            print("Claim ID:", claim["claim_id"])
            print("Customer:", claim["name"])
            print("Product:", claim["product_name"])
            print("Receipt Number:", claim["receipt_no"])
            print("Reported Issue:", claim["issue"])
            print("Claim Date:", claim["claim_date"])
            print("Status:", claim["status"])

            if claim["resolution_type"]:
                print("Resolution:", claim["resolution_type"])

        print("----------------------------------------")

    except sqlite3.Error as error:
        print("\nDatabase Error:", error)



def review_claim():

    print("\n========== REVIEW WARRANTY CLAIM ==========")

    claim_id = get_claim_id()

    try:

        with connect_db() as conn:

            claim = conn.execute("""
                SELECT *
                FROM claims
                WHERE claim_id = ?
            """, (claim_id,)).fetchone()

            if claim is None:
                print("\nError: Claim record not found.")
                return

            if claim["status"] != "Pending":
                print("\nThis claim has already been reviewed.")
                print("Current Status:", claim["status"])
                return

            print("\nReported Issue:", claim["issue"])
            print("Claim Date:", claim["claim_date"])

            print("\n1. Approve Claim")
            print("2. Reject Claim")

            choice = input("Select Decision: ").strip()

            if choice == "1":
                status = "Approved"

            elif choice == "2":
                status = "Rejected"

            else:
                print("\nInvalid selection.")
                return

            conn.execute("""
                UPDATE claims
                SET status = ?
                WHERE claim_id = ?
            """, (status, claim_id))

        print("\nClaim successfully reviewed!")
        print("New Status:", status)

    except sqlite3.Error as error:
        print("\nDatabase Error:", error)


def record_resolution():

    print("\n========== RECORD CLAIM RESOLUTION ==========")

    claim_id = get_claim_id()

    try:

        with connect_db() as conn:

            claim = conn.execute("""
                SELECT *
                FROM claims
                WHERE claim_id = ?
            """, (claim_id,)).fetchone()

            if claim is None:
                print("\nError: Claim record not found.")
                return

            if claim["status"] != "Approved":
                print("\nOnly approved claims can be completed.")
                print("Current Status:", claim["status"])
                return

            print("\n1. Repair")
            print("2. Replacement")

            choice = input("Select Resolution: ").strip()

            if choice == "1":
                resolution = "Repair"

            elif choice == "2":
                resolution = "Replacement"

            else:
                print("\nInvalid selection.")
                return

            notes = get_required_input(
                "Enter Resolution Details: "
            )

            conn.execute("""
                UPDATE claims
                SET status = 'Completed',
                    resolution_type = ?,
                    resolution_notes = ?
                WHERE claim_id = ?
            """, (resolution, notes, claim_id))

        print("\nClaim successfully completed!")
        print("Resolution:", resolution)
        print("Details:", notes)
        print("Status: Completed")

    except sqlite3.Error as error:
        print("\nDatabase Error:", error)



def view_reports():

    print("\n========== TRANSACTION REPORTS ==========")

    try:

        with connect_db() as conn:

            total_customers = conn.execute("""
                SELECT COUNT(*) AS total
                FROM customers
            """).fetchone()["total"]

            total_purchases = conn.execute("""
                SELECT COUNT(*) AS total
                FROM purchases
            """).fetchone()["total"]

            total_claims = conn.execute("""
                SELECT COUNT(*) AS total
                FROM claims
            """).fetchone()["total"]

            pending = conn.execute("""
                SELECT COUNT(*) AS total
                FROM claims
                WHERE status = 'Pending'
            """).fetchone()["total"]

            approved = conn.execute("""
                SELECT COUNT(*) AS total
                FROM claims
                WHERE status = 'Approved'
            """).fetchone()["total"]

            rejected = conn.execute("""
                SELECT COUNT(*) AS total
                FROM claims
                WHERE status = 'Rejected'
            """).fetchone()["total"]

            completed = conn.execute("""
                SELECT COUNT(*) AS total
                FROM claims
                WHERE status = 'Completed'
            """).fetchone()["total"]

        print("\nCUSTOMER STATISTICS")
        print("Total Customers:", total_customers)

        print("\nPURCHASE STATISTICS")
        print("Total Purchases:", total_purchases)

        print("\nWARRANTY CLAIM STATISTICS")
        print("Total Claims:", total_claims)
        print("Pending Claims:", pending)
        print("Approved Claims:", approved)
        print("Rejected Claims:", rejected)
        print("Completed Claims:", completed)

        print("\n========================================")

    except sqlite3.Error as error:
        print("\nDatabase Error:", error)



def main():

    initialize_database()

    while True:

        print("\n")
        print("==========================================")
        print("             WARRANTIE")
        print("    PRODUCT WARRANTY MANAGEMENT")
        print("==========================================")

        print("1. Register New Purchase")
        print("2. Search Purchase")
        print("3. Submit Warranty Claim")
        print("4. View All Claims")
        print("5. Review Claim")
        print("6. Record Repair or Replacement")
        print("7. View Transaction Reports")
        print("8. Exit")

        print("==========================================")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            register_purchase()

        elif choice == "2":
            search_purchase()

        elif choice == "3":
            submit_claim()

        elif choice == "4":
            view_claims()

        elif choice == "5":
            review_claim()

        elif choice == "6":
            record_resolution()

        elif choice == "7":
            view_reports()

        elif choice == "8":
            print("\nThank you for using WarranTie!")
            print("Program terminated.")
            break

        else:
            print("\nInvalid choice. Please select 1-8.")



if __name__ == "__main__":
    main()
