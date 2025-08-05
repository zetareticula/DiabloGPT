-- Simple test queries for MUMFORDGRAMMAR
SELECT * FROM table1 WHERE col1 > 10 AND col2 < 50;
SELECT * FROM table1 WHERE col3 = 'test' AND col4 BETWEEN 100 AND 200;
SELECT * FROM table1 WHERE col5 IN (1, 2, 3) OR col6 > 1000;
