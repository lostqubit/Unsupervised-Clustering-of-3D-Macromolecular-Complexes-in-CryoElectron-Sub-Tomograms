import os
import numpy as np
import pandas as pd
import mrcfile
import torch
from torch.utils.data import Dataset


class Subtomograms(Dataset):
	def __init__(self,dataset):
		# dataset == 'train' or 'test'

		self.dataset = dataset
		assert dataset in ['train','test']

		base_dir =  os.path.join(os.getcwd(), 'data')

		self.dataset_dir = os.path.join(base_dir,dataset)
		self.subtomograms = os.listdir(self.dataset_dir)
		if dataset == 'train':
			self.labels = pd.read_csv(os.path.join(base_dir,'train_labels.csv'),header = 0,index_col = 0)
			print(self.labels.head())
		else:
			self.labels = pd.read_csv(os.path.join(base_dir,'test_labels.csv'),header = 0,index_col = 0)
		self.label_meanings = self.labels.columns.values.tolist()

	def __len__(self):

		return len(self.subtomograms)

	def __getitem__(self, index):

		subtomogram = self.subtomograms[index]
		with mrcfile.open(os.path.join(self.dataset_dir,subtomogram)) as f:
			subtomogram_data = f.data
			f.close()

		#convert data to tensor and rescale voxels b/w 0 and 1
		subtomogram_processed = torch.Tensor(subtomogram_data)
		subtomogram_processed = subtomogram_processed.view(1,24,24,24)

		rescale = tio.RescaleIntensity(out_min_max=(0, 1))
		subtomogram_processed = rescale(subtomogram_processed)
        
		#load label
		label = torch.Tensor(self.labels.loc[subtomogram,:].values)

		item = {'data': subtomogram_processed, 'label':label,'index':index}

		return item

