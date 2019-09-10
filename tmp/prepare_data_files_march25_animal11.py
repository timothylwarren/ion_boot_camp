

#read in 
import file_utilities as util
import pdb
import pickle
import filehandling as fh
outfile='alldt_stream.pck'
data_path='/users/tim/data/2ptmp/may20/'
dtfiles=['stream_ex_dt.tif']
list_of_tifstacks=[]
sumdt={}
meta_dt={}


for ind,crfile in enumerate(dtfiles):
    
    (im,stim)=util.read_in_tif_and_get_metadata(data_path + crfile)
    if ind==0:
        dt=fh.open_pickle(data_path+crfile+'.pck')
    pdb.set_trace()
    frames_to_keep=slice(10,1280)
    
    xzoom=slice(100,180)
    yzoom=slice(190,280)
    sliced_tif=im['tifstack'][frames_to_keep,xzoom,yzoom]
    meta_dt['stim_edges']=dt['stim_edges']
    meta_dt['stim_zoom_vls']=dt['zoom_vls']
    meta_dt['xzoom']=xzoom
    meta_dt['yzoom']=yzoom
    meta_dt['frames_to_keep']=frames_to_keep
    list_of_tifstacks.append(sliced_tif)
outfile = open(data_path+outfile,'wb')
sumdt['list_of_tifstacks']=list_of_tifstacks
sumdt['meta_dt']=meta_dt
pickle.dump(sumdt,outfile)
outfile.close()