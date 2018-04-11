CREATE DEFINER=`diaasmaster`@`%` PROCEDURE `spWorkSpaceDetails`(
IN user_id smallint(6)
)
BEGIN
select ID,WORKSPACE_TITLE from docDD_Workspace_Master_Table;
end