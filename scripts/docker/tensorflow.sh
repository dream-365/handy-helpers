# jupter + tensorflow 2.5.1 (CPU)
docker run --name tf-jupyter \
-d -v $(realpath ~/notebooks/):/tf/notebooks \
-p 8008:8888 \
registry-vpc.cn-hangzhou.aliyuncs.com/hz-ns1/tensorflow:2.5.1

# tensorflow serving 2.5.1 (CPU)
docker run --name tf-serving \
-dt \
-v $(realpath ~/notebooks/rec/model):/models \
-p 8501:8501 \
registry-vpc.cn-hangzhou.aliyuncs.com/hz-ns1/tf-serving:2.5.1-devel \
tensorflow_model_server --port=8500 --rest_api_port=8501 \
--model_name=${model_name} --model_base_path=${model_base_path}