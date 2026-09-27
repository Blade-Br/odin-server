import json

from database.conexaobd import iniciar_banco


def gravar_inventario(inventario):
    """Grava os dados estáticos da máquina no banco de dados."""

    conexao = iniciar_banco()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO maquinas (
            uuid,
            hostname,
            sistema_operacional,
            versao_so,
            nucleos_fisicos,
            nucleos_logicos,
            memoria_fisica,
            memoria_virtual,
            modelo_cpu
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
    """

    valores = (
        str(inventario.maquina_id),
        inventario.identificacao.hostname,
        inventario.identificacao.sistema_operacional,
        inventario.identificacao.versao,
        inventario.cpu.nucleos_fisicos,
        inventario.cpu.nucleos_logicos,
        inventario.memoria.memoria_fisica.capacidade_total_gb,
        inventario.memoria.memoria_virtual.capacidade_total_gb,
        inventario.cpu.modelo
    )

    cursor.execute(sql, valores)

    gravar_discos(
        cursor,
        inventario.maquina_id,
        inventario.discos
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def gravar_discos(cursor, maquina_id, discos):
    """Grava os discos pertencentes à máquina."""

    sql = """
        INSERT INTO discos (
            maquina_uuid,
            nome,
            capacidade_total,
            tipo_disco
        )
        VALUES (
            %s, %s, %s, %s
        )
    """

    for disco in discos:
        valores = (
            str(maquina_id),
            disco.nome,
            disco.capacidade_total_gb,
            disco.tipo
        )

        cursor.execute(sql, valores)


def gravar_metricas(metricas):
    """Grava os dados voláteis das métricas no banco de dados."""

    conexao = iniciar_banco()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO metricas_maquina (
            maquina_uuid,
            coletado_em,
            cpu_uso_percentual,
            cpu_frequencia_ghz,
            cpu_uso_por_nucleo,
            memoria_fisica_utilizada_gb,
            memoria_fisica_utilizada_percentual,
            memoria_fisica_disponivel_gb,
            memoria_fisica_disponivel_percentual,
            memoria_virtual_utilizada_gb,
            memoria_virtual_utilizada_percentual,
            memoria_virtual_disponivel_gb,
            memoria_virtual_disponivel_percentual,
            rede_conectado,
            rede_nome,
            rede_ipv4,
            rede_download_mb_s,
            rede_upload_mb_s,
            uptime_segundos
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
    """

    valores = (
        str(metricas.maquina_id),
        metricas.timestamp,
        metricas.cpu.uso_percentual,
        metricas.cpu.frequencia_ghz,
        json.dumps(metricas.cpu.uso_por_nucleo),
        metricas.memoria.memoria_fisica.memoria_utilizada_gb,
        metricas.memoria.memoria_fisica.memoria_utilizada_percentual,
        metricas.memoria.memoria_fisica.memoria_disponivel_gb,
        metricas.memoria.memoria_fisica.memoria_disponivel_percentual,
        metricas.memoria.memoria_virtual.memoria_utilizada_gb,
        metricas.memoria.memoria_virtual.memoria_utilizada_percentual,
        metricas.memoria.memoria_virtual.memoria_disponivel_gb,
        metricas.memoria.memoria_virtual.memoria_disponivel_percentual,
        metricas.rede.conectado,
        metricas.rede.nome_rede,
        str(metricas.rede.ipv4) if metricas.rede.ipv4 else None,
        metricas.rede.download_mb_s,
        metricas.rede.upload_mb_s,
        metricas.sistema.uptime_segundos
    )

    cursor.execute(sql, valores)

    metrica_maquina_id = cursor.lastrowid

    gravar_metricas_discos(
        cursor,
        metrica_maquina_id,
        metricas.maquina_id,
        metricas.discos
    )

    conexao.commit()

    cursor.close()
    conexao.close()


def gravar_metricas_discos(
    cursor,
    metrica_maquina_id,
    maquina_id,
    discos
):
    """Grava as métricas dos discos da máquina."""

    sql_buscar_disco = """
        SELECT id
        FROM discos
        WHERE maquina_uuid = %s
          AND nome = %s
    """

    sql_gravar = """
        INSERT INTO metricas_disco (
            metrica_maquina_id,
            disco_id,
            utilizado_gb,
            disponivel_gb
        )
        VALUES (
            %s, %s, %s, %s
        )
    """

    for disco in discos:

        cursor.execute(
            sql_buscar_disco,
            (
                str(maquina_id),
                disco.nome
            )
        )

        resultado = cursor.fetchone()

        if resultado is None:
            raise ValueError(
                f"Disco '{disco.nome}' não encontrado "
                "para a máquina."
            )

        disco_id = resultado[0]

        valores = (
            metrica_maquina_id,
            disco_id,
            disco.utilizado_gb,
            disco.disponivel_gb
        )

        cursor.execute(sql_gravar, valores)