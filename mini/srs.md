# SRS for Library Management Application

## 1. Introduction
The Library Management Application is a comprehensive software solution designed to cater to the needs of library users, employees and administrators. The application focuses solely on managing the library's core functions such as book borrowing, returning, inventory management , and user management. The repairs and budget management are outsourced to contractors and separate software solutions, respectively. It is intended to be implemented as a web application or as an installable application on computers and smartphones that accesses the library server. The application relies heavily on a database system with locking and notification support to avoid inconsistencies in data across different instances of the application.
## 2. Database structure
The database structure is crucial to the application's functionality and security. The following databases should be implemented with appropriate normalization and indexing to ensure data consistency and performance:
1. `Books` and `BookCopies` 
	- `Books` - stores information about all the books in the library.
	- `BookCopies` - stores information about each physical copy of a book in the library.
	- A single book can have multiple editions available in the library, so a separate database for book copies is required.
2. Availability-based details on copies
	- `BorrowedCopies` - stores information about all the copies that are currently checked out by users.
	- `ReservedCopies` - stores information about all the copies that have been reserved by users. 
	- To avoid inconsistencies when multiple users try to access the same book copy simultaneously, the `BorrowedCopies` and `ReservedCopies` database should be accessed with locking mechanisms on.
	- `OrderedCopies` - stores information about all the books ordered by the library.
3. Book details
	- `Authors` - stores information about all the authors of the books in the library.
	- `Publishers` - stores information about all the publishers of the books in the library.
	- `Genres` - stores information about all the genres of the books in the library.
	- `Subjects` - stores information about all the subjects of the books in the library.
	- `Languages` - stores information about all the languages in which the book copies in the library are available.
3. `Localization` 
	- maintains a comprehensive record of all library locations to facilitate accurate tracking of copies to their specific shelves or storage locations.
4. Financial:
	- `Payments` - This database stores information about payments made by users, including payment amount and date.
	- `OutstandingPayments`- This database stores information about any outstanding payments owed by users for items such as overdue books or damaged copies.
	- `PaymentsMethod` - stores information about all the payment methods accepted by the library, for example, credit card or cash.
	- `Receipts` - This database stores information about receipts generated for users, including the payment amount, date, and any relevant transaction details.
5. User-related:
	- `Users` - stores information about all the library users.
	- `ElevatedUsers` - stores information about all the elevated users, for example, staff members or administrators, who have special privileges in the library system.
	- `Permissions` - stores information about all the permissions granted to each user in the library system. Additional privileges may be automatically granted to elevated users, while certain privileges may be revoked if the user has been suspended.
	- `LoginAttempts` - stores information about all the login attempts made by standard or elevated users in the library system.
	- `UserBans` - stores information about all banned users and the reasons for the ban. Bans can be given out automatically based on the number of login attempts within a given timeframe or whether there's an overdue return or overdue payment.
## 3. Functionalities

### 3.1. Functionalities without Logging In
By default, the application supports the following features without logging in:
1. `Search` bar for books:
	- Search can be performed by title, author, publisher, genre or subject.
	- A filter is available with various options such as language or availability.
2. `Localization` and `Contact` buttons.
3. `Log In` button:
	- Sign Up functionality is not present, as users can only sign up by physically visiting a library.

### 3.2. Logging In
1. The user logs in by providing an email and password. Every login attempt is stored, and the user can be temporarily locked if there are too many login attempts. Only the hash of passwords is stored in the database to ensure data security.
2. If a user forgets their password, there is a password reset functionality based on sending a generated confirmation code to the user's email address. If the code is correct, the user can set a new password.
3. After logging in, the user's privileges are based on the level of their user account and the permissions defined for that account.

### 3.3 User Account
For a standard logged-in library user, the following functionalities are available:
1. Displaying the list of borrowed books with relevant information such as the return date and limited ability to prolong the return date.
2. Reserving a book copy for a specific date.
3. Payments
	- Standard users can view a list of outstanding payments in their personal account, including fees for:
		- Library card issuance.
		- Damaged books. 
		- Overdue returns.
	- Fees can be payed either through online transaction services or via a bank transfer with the information provided. 
4. Editing profile settings.

### 3.4. Employee Account
For a logged-in employee, the following functionalities are available:
1. Registrating standard users
	- To provide standard users with access to the library system, employees can facilitate their registration by creating a personal account and entering required information such as their email address, name, surname, and PESEL number. 
	- Additionally, a plastic card confirming their registration is issued, and a fee for card issuance is added to the user's account.
2. Accepting the payments for outstanding fees listed in the user's account, including fees for:
	- Library card issuance.
	- Damaged books.
	- Overdue returns.
3. Changing the status of a particular copy of a book, which includes cases of a returned copy or a damaged book.
4. Limited ability to extend the return date of a book copy, which may automatically withdraw penalties
5. Limited ability to impose penalties on users who violate the return date or damage a book copy. 
	- The penalties include restrictions on the ability to borrow books and fines.

### 3.5. Admin Account
For a logged-in admin, the following functionalities are available:
1. Inventory management
	- Adding, removing, and editing book-related databases.
	- Modifying availability status in case of damaged or reserved copies.
2. Repair management:
	- Changing the status of repairs, such as "in-progress" or "completed".
	- Imposing penalties on users who damage or mishandle library books.
3. User management:
	- Adding and removing users.
	- Blocking and unblocking users.
	- Limited ability to change user preferences, such as resetting passwords or changing PESEL numbers.
4. Penalty management:
	- Imposing and withdrawing penalties.
	- Extending return dates or outstanding payment dates, which may automatically withdraw penalties.
	- Violation management, including updating debtor status, such as "case referred to the legal team".
5. Elevated account management (for library staff):
	- Promoting and demoting user accounts to elevated user accounts.
	- Changing the permissions of elevated users.
