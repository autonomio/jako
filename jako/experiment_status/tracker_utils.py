def setup_graphql(self, client, machine_id):

    execute_strings = ['sh /tmp/jako_docker_compose.sh',
                       'sudo docker compose -f /tmp/docker-compose.yml up -d'
                       ]

    for execute_str in execute_strings:
        stdin, stdout, stderr = client.exec_command(execute_str)
        if stderr:
            for line in stderr:
                try:
                    # Process each error line in the remote output
                    print(line)
                except Exception as e:
                    print(e)

        for line in stdout:
            try:
                # Process each line in the remote output
                print(line)
            except Exception as e:
                print(e)
