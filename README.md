In this project, I build a LSTM-RNN to predict stock prices using keras with tensorflow. The training data comes from historical closing precies of S&P500. The accuracy measured by Root Mean Square Error (RMSE) is around 0.99. And I did experiments on the network's hyper-parameters such as LSTM cell hidden state size, truncated back propagation length and depth of the network.
At last, I build a website using this prediction model as engine with Flask and python.

# Dependencies:
python 2.7
pip 9.0.1
flask 0.12.1

tensorflow 0.12.1
keras1.2.1

# Run:
Note: Please activate tensorflow virtual env first.

To runthe experiment on LSTM structures:
> cd ./model

> python experiment.py

To run the web app, first change back to the root
> python app.py

# Paper & vedio demo
* paper: https://github.com/hualiu01/LSTMRNNStockr/blob/master/paper.pdf
* YouTube vedio demo: https://www.youtube.com/watch?v=haou7Se-RIs&feature=youtu.be



