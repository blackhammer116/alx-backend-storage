-- getting the bands with the highest fans with their origin
SELECT origin, fans AS nb_fans FROM metal_bands ORDER BY nb_fans DESC;
