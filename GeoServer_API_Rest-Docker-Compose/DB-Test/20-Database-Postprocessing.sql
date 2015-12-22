\c test_geoserver postgres localhost 5435

alter table data.municipio
add column area float;

update data.municipio
set area=round(st_area(geom)::numeric, 2)::float;

vacuum analyze;
