--ALTER TABLE auth_user
  --ADD phone VARCHAR;

--UPDATE auth_user 
--SET 
  --phone = '66338811'
--WHERE
  --id = 1;

UPDATE cart_cartorderdetail 
SET 
  item_id = 5
WHERE
  id = 4;

--DELETE FROM auth_user
--WHERE id = 3;