CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT c.name, c.phone FROM phonebook c
                 WHERE c.name ILIKE '%' || p || '%'
                    OR c.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paged(lim int, off int)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT c.name, c.phone FROM phonebook c
                 ORDER BY c.name
                 LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;
