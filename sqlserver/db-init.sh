STATE=0
until [ $STATE -eq 1 ]; do
    echo "Trying to execute init script"
    /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $SA_PASSWORD -d master -i db-init.sql && STATE=1
    if [ $STATE -ne 1 ]; then
        echo "\t[ ]Error executing init script"
        sleep 1
    else
        echo "\t[*]Success executing init script"
    fi
done