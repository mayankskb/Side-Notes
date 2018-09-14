from cassandra.cluster import Cluster
from cassandra import ReadTimeout

cluster = Cluster()
session = cluster.connect()

keyspace_name = session.execute('SELECT * FROM system_schema.keyspaces')

print("-" * 70)
for name in keyspace_name:
	print(name)
print('-' * 70)

print('\n\n')

session.set_keyspace('student')

output = session.execute('SELECT * FROM subject_list')

print('-' * 70)
for row in output:
    print(row)
print('-' * 70)

print('\n\n')

print('-' * 70)
rows = session.execute('SELECT sub_name, max_marks, pass_marks FROM subject_list')
for row in rows:
	print('{0} -- {1} -- {2}'.format(row.sub_name, row.max_marks, row.pass_marks))
print('-' * 70)

# Making an asynchronous query
sub_id = [12, 1, 2, 10, 7, 8]
futures = []
query = 'SELECT * FROM subject_list WHERE id=%s'

for iid in sub_id:
	futures.append(session.execute_async(query, [iid]))

print('Fed the async query, the output is not printed.')
print('Calling the ResponseFuture object of async query')

try:
	for future in futures:
		rows = future.result()
		subject = rows[0]
		print('Subject Name : ', subject.sub_name, 'Subject Passing Marks : ', subject.pass_marks)
except ReadTimeout:
	log.exception('Query Read timed out:')




print('-' * 70)

def handle_success(rows, label):
	subject = rows[0]
	try:
		print(label,' : ',' Subject Name : ',subject.sub_name, ' Passing Marks : ', subject.pass_marks, ' Max Marks : ', subject.max_marks)
	except Exception:
		log.error('Failed to process subject %s', subject.id)

def handle_error(exception):
	log.error('Failed to fetch subject info: %s', exception)

sid = int(input('Enter the subject id : '))

futures = session.execute_async(query, [sid])
futures.add_callback(handle_success, 'Async Call')
futures.add_errback(handle_error)

print('Fed the async query, the output is not printed.')
print('Calling the ResponseFuture object of async query')

query_result = futures.result()