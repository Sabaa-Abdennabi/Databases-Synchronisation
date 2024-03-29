# GUIDE TO MAKE THIS TP WORK
# RA7MOULI AALE WALDEYE W SHOKRAN 
1. **Download MySQL Server**: 
    - Visit the [MySQL Downloads](https://dev.mysql.com/downloads/mysql/) page.
    - Choose the appropriate version for your operating system and download MySQL Server.

2. **Download the Requirements**: 
    - Open your terminal or command prompt.
    - Run the following commands to install the required Python packages:
        ```bash
        pip install pika
        pip install mysql-connector-python
        pip install pymysql
        ```

3. **Open MySQL Server**: 
    - Once MySQL Server is installed, open it using your preferred method.

4. **Run Commands in MySQL Server**:
    - Open MySQL Server and run the following commands:
        ```sql
        -- Replace "path_to_BO1.sql" with the actual path of the file
        source "path_to_BO1.sql";
        
        -- Do the same for BO2 and HO_database
        use BO1_database;
        
        DELIMITER //

        CREATE PROCEDURE capture_product_sales_changes(IN query VARCHAR(2000))
        BEGIN
        -- Write the captured query to a file
        INSERT INTO product_sales_changes_log (query, created_at)
        VALUES (query, NOW());
        END //

        DELIMITER ;

        CREATE TABLE product_sales_changes_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            query VARCHAR(2000) NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        DELIMITER //

        CREATE TRIGGER product_sales_insert_trigger
        AFTER INSERT ON product_sales
        FOR EACH ROW
        BEGIN
        DECLARE sql_stmt VARCHAR(2000);
        SET sql_stmt = CONCAT('INSERT INTO product_sales (date, region, product, qty, cost, amount, tax, total) VALUES (\'', NEW.date, '\', \'', NEW.region, '\', \'', NEW.product, '\', ', NEW.qty, ', ', NEW.cost, ', ', NEW.amount, ', ', NEW.tax, ', ', NEW.total, ');');
        -- Call the stored procedure to log the captured statement
        CALL capture_product_sales_changes(sql_stmt);
        END //

        CREATE TRIGGER product_sales_update_trigger
        AFTER UPDATE ON product_sales
        FOR EACH ROW
        BEGIN
        DECLARE sql_stmt VARCHAR(2000);
        SET sql_stmt = CONCAT('UPDATE product_sales SET date = \'', NEW.date, '\', region = \'', NEW.region, '\', product = \'', NEW.product, '\', qty = ', NEW.qty, ', cost = ', NEW.cost, ', amount = ', NEW.amount, ', tax = ', NEW.tax, ', total = ', NEW.total, ' WHERE date = \'', OLD.date, '\' AND region = \'', OLD.region, '\' AND product = \'', OLD.product, '\';');
        -- Call the stored procedure to log the captured statement
        CALL capture_product_sales_changes(sql_stmt);
        END //

        CREATE TRIGGER product_sales_delete_trigger
        AFTER DELETE ON product_sales
        FOR EACH ROW
        BEGIN
        DECLARE sql_stmt VARCHAR(2000);
        SET sql_stmt = CONCAT('DELETE FROM product_sales WHERE date = \'', OLD.date, '\' AND region = \'', OLD.region, '\' AND product = \'', OLD.product, '\';');
        -- Call the stored procedure to log the captured statement
        CALL capture_product_sales_changes(sql_stmt);
        END //

        DELIMITER ;
        ```
    - For BO2, use `BO2_database` instead of `BO1_database` and run the same commands for BO2 database too.

5. **Make Modifications in Your Databases (BO1 and BO2)**: 
    - Make some changes :insert delete update in your databases BO1 and BO2.

6. **Synchronize Databases**:
    - Run the `synchronize.py` file for BO1:
        ```bash
        python synchronize.py
        ```
    - Run the `BO1.py` file:
        ```bash
        python BO1.py
        ```
    - Repeat the same steps for BO2.
    - Finally, run the `HO.py` file:
        ```bash
        python HO.py
        ```

Your HO table is now synchronized! You can verify the synchronization in your MySQL databases. 

RA7MOULI AALE WALDEYA 
