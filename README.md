## TEST ###

<pre><code>
curl -X GET http://127.0.0.1:7000/api/v1.0/blueprint

curl -X GET http://127.0.0.1:7000/api/v1.0/blueprint/1

curl -H "Content-Type: application/json" -X POST -d '{"name":"abc","components":"hbase,spark","rolename":"3,0,0","content":{"ambari":"hadoop"}}' http://127.0.0.1:7000/api/v1.0/blueprint

curl -H "Content-Type: application/json" -X PUT -d '{"name":"aaa","components":"hbase,spark","rolename":"3,0,0","content":{"ambari":"hadoop"}}' http://127.0.0.1:7000/api/v1.0/blueprint/1

curl -X DELETE http://127.0.0.1:7000/api/v1.0/blueprint/1

curl -X GET http://127.0.0.1:7000/api/v1.0/blueprintsave/1

</code></pre>

