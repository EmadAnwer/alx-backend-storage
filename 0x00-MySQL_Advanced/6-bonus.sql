--  stored procedure AddBonus that adds a new correction for a student.


DELIMITER //
CREATE PROCEDURE AddBonus(IN user_id, IN project_name, IN score)
BEGIN
    IF (SELECT id FROM projects WHERE name = project_name) IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET @project_id = LAST_INSERT_ID();
    ELSE
        SELECT id INTO @project_id FROM projects WHERE name = project_name;
    END IF;

    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, @project_id, score);

END //

DELIMITER ;
