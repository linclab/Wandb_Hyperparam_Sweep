"""
This script receives hyperparameters from the Wandb agent, and then launches 3 train.py processes by calling the 
wandb_run_train.sh script
"""

import argparse
import os
import wandb
import sys

if __name__=='__main__':

	# Process all of the arguments generated by the Wandb sweep agent
	parser = argparse.ArgumentParser(description="Process hyperparameters generated by Wandb sweep agent") # create ArgumentParser object
	parser.add_argument("--task",type=str,default='go',help="Cognitive task being peformed,e.g. go")
	parser.add_argument("--hidden_dim",type=int,default=20,help="Input hidden dimension size") #J
	parser.add_argument("--non_linearity",type=str,default='relu',help="RNN non-linearity")
	parser.add_argument("--mode",type=str,default='BPTT',help="Temporal credit assignment algorithm")
	parser.add_argument("--noise",type=str,default='sparse',help="Type of noise to be added to backward weights")
	parser.add_argument("--epochs",type=int,default=500,help="Number of training epochs")
	parser.add_argument("--lr",type=float,default=1e-3,help="Learning rate value")
	parser.add_argument("--momentum",type=float,default=0.0,help="Momentum value")
	parser.add_argument("--gc",type=int,default=100,help="Gradient clipping value")
	parser.add_argument("--save_results",default=False,action='store_true',help="Add to save plots and results in file, else hyperparameter search with Wandb is run") #J

	ns, unknown_args = parser.parse_known_args()
	if len(unknown_args)==0:
		args = parser.parse_args()
		argsdict = args.__dict__
	else:
		print("Unknown arguments are provided. Please check and try again.")
		sys.exit()

	print(argsdict)
	task = argsdict["task"]
	hidden_dim = argsdict["hidden_dim"]
	non_linearity = argsdict["non_linearity"]
	mode = argsdict["mode"]
	noise = argsdict["noise"]
	n_epochs = argsdict["epochs"]
	lr = argsdict["lr"]
	momentum = argsdict["momentum"]
	gc = argsdict["gc"]
	save_results = argsdict["save_results"]

	sweep_run = wandb.init(settings=wandb.Settings(start_method="fork")) # Set starting method to avoid well-documented error: https://docs.wandb.ai/guides/track/launch#init-start-error
	sweep_id = sweep_run.sweep_id or "unknown"
	project_url = sweep_run.get_project_url()
	sweep_group_url = "{}/groups/{}".format(project_url, sweep_id)
	sweep_run.notes = sweep_group_url
	sweep_run.save()
	sweep_run_name = sweep_run.name or sweep_run.id or "unknown"

	print("*" * 40)
	print("sweep_id: ", sweep_id)
	print("Sweep Group URL: ", sweep_group_url)
	print("Sweep_run_name: ", sweep_run_name)
	print("*" * 40)

	#command_1 = './wandb_run_train.sh {} {} {} {} {} {} {} {} {} {}'.format(n_epochs, gc, hidden_dim, lr, mode, momentum, non_linearity, seq_length, sweep_id, sweep_run_name) # use this if you're not running sbatch
	command_1 = 'sbatch wandb_run_train.sh {} {} {} {} {} {} {} {} {} {}'.format(n_epochs, gc, hidden_dim, lr, mode, momentum, non_linearity, task, sweep_id, sweep_run_name) # use this if you are running sbatch

	# Launch a Bash script to launch 3 train.py processes
	os.system(command_1)
	
