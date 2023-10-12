-- creating a trigger on update
DELIMITER :
CREATE TRIGGER refuse_update2 BEFORE UPDATE ON users
FOR EACH ROW
	BEGIN
		IF OLD.email <> NEW.email THEN
			SET NEW.valid_email = 0;
		END IF;
	END:
DELIMITER ;
