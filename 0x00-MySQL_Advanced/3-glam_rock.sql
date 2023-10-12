-- getting the band name and lifespan
SELECT band_name, TIMESTAMPDIFF(YEAR, formed, IFNULL(split, '2022')) AS lifespan FROM metal_bands WHERE style = 'Glam rock' ORDER BY lifespan DESC;
