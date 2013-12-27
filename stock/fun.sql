delimiter $$
CREATE FUNCTION getstockid(stockcode varchar(255))
RETURNS int
DETERMINISTIC
BEGIN
  DECLARE stockid int;
  SET stockid = (SELECT id FROM StockTradeRecord_stock WHERE code = stockcode);
  RETURN stockid;
END$$


CREATE FUNCTION getindustryid(stockcode varchar(255))
RETURNS int
DETERMINISTIC
BEGIN
  DECLARE stockid int;
  SET stockid = (SELECT id FROM StockTradeRecord_industry WHERE name = stockcode);
  RETURN stockid;
END$$

CREATE FUNCTION getregionid(stockcode varchar(255))
RETURNS int
DETERMINISTIC
BEGIN
  DECLARE stockid int;
  SET stockid = (SELECT id FROM StockTradeRecord_region WHERE name = stockcode);
  RETURN stockid;
END$$


delimiter ;
