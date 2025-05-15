USE quizo;

-- Modify the columns to allow longer values
ALTER TABLE sign_up
MODIFY COLUMN username varchar(50) NOT NULL,
MODIFY COLUMN password varchar(100) NOT NULL;

-- Add a comment to explain the changes
ALTER TABLE sign_up COMMENT = 'Updated column lengths for better user experience'; 