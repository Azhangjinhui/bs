#1.构建流式执行环境
from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment, RuntimeExecutionMode, DataStream
from pyflink.table import DataTypes

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
# env.set_runtime_mode(RuntimeExecutionMode.STREAMING)
#2.数据source
input_ds = DataStream(env._j_stream_execution_environment.socketTextStream("172.26.251.216",9999))
#3.数据处理
result_ds = input_ds.flat_map(lambda x:x.split(" ")) \
	.map(lambda word:(word,1),output_type=Types.TUPLE([Types.STRING(),Types.INT()])). \
	key_by(lambda x:x[0]) \
	.reduce(lambda x,y:(x[0],x[1] + y[1]))
#4.数据Sink
result_ds.print()
#5.启动流式任务
env.execute()