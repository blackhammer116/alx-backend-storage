--getting the bands with the highest fans with their origin
ALTER TABLE metal_bands CHANGE fans nb_fans INT(11);
SELECT origin, nb_fans FROM metal_bands ORDER BY nb_fans DESC;
