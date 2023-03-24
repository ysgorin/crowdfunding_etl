-- Contacts Table Schema
CREATE TABLE Contacts (
    contact_id INT,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    PRIMARY KEY (contact_id)
);

-- Category Table Schema
CREATE TABLE Category (
    category_id CHAR(4),
    category VARCHAR NOT NULL,
    PRIMARY KEY (category_id)
);

-- Subcategory Table Schema
CREATE TABLE Subcategory (
    subcategory_id VARCHAR(8),
    subcategory VARCHAR NOT NULL,
    PRIMARY KEY (subcategory_id)
);

-- Campaign Table Schema
CREATE TABLE Campaign (
    cf_id INT,
    contact_id INT,
    company_name VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    goal FLOAT NOT NULL,
    pledged FLOAT NOT NULL,
    backers_count INT NOT NULL,
    country CHAR(2) NOT NULL,
    currency CHAR(3) NOT NULL,
    launched_date DATE NOT NULL,
    end_date DATE NOT NULL,
    category_id CHAR(4),
    subcategory_id VARCHAR(8),
    PRIMARY KEY (cf_id),
    FOREIGN KEY (contact_id) REFERENCES Contacts(contact_id),
    FOREIGN KEY (category_id) REFERENCES Category(category_id),
    FOREIGN KEY (subcategory_id) REFERENCES Subcategory(subcategory_id)
);