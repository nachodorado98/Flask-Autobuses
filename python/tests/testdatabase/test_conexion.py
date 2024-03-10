def test_conexion(conexion):

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()["current_database"]=="bbdd_buses"

	conexion.c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

	tablas=[tabla["relname"] for tabla in conexion.c.fetchall()]

	assert "lineas" in tablas
	assert "paradas" in tablas
	assert "barrios" in tablas

def test_cerrar_conexion(conexion):

	assert not conexion.bbdd.closed

	conexion.cerrarConexion()

	assert conexion.bbdd.closed

def test_tabla_lineas_llena(conexion):

	conexion.c.execute("SELECT * FROM lineas")

	assert conexion.c.fetchall()

def test_tabla_paradas_llena(conexion):

	conexion.c.execute("SELECT * FROM paradas")

	assert conexion.c.fetchall()

def test_tabla_barrios_llena(conexion):

	conexion.c.execute("SELECT * FROM barrios")

	assert conexion.c.fetchall()