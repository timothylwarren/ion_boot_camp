#file_utilities.py
#series of functions useful for manipulating slidebook files

import skimage.io
import xmltodict
import numpy as np
import  pdb


def read_in_tif(filename):
    im={}
    im['tifstack']=skimage.io.imread(filename)
    return im

def read_in_tif_and_get_metadata(filename):
    time_between_frames=.12625
    im={}
    stim={}
    im['tifstack']=skimage.io.imread(filename)
    num_frames=np.shape(im['tifstack'])[0]
    im['time_stamps']=np.linspace(time_between_frames,time_between_frames*num_frames,num_frames)

    (im['erroneous_time_stamps'],im['frame_nums'],stim['stim_frame_nums'])=get_time_stamps(filename)
    
    return(im,stim)


def make_edges(xvls,yvls,imzoom):
    zero_im=np.zeros(np.shape(imzoom))
    
    zero_im[yvls,xvls]=1
    edges=edge_detector(zero_im)
    return edges


def edge_detector(im): 
    from skimage import feature
    edges = feature.canny(im)
    return (edges)
    
def get_time_stamps(filename):
    time_stamps=[]
    image_frame_nums=[]
    stim_times=[]
    
    with open (filename + '.xml') as fd: 
        doc=xmltodict.parse(fd.read())
      
        all_planes=doc['OME']['Image']['Pixels']['Plane']
    
        for crplane in all_planes:

            time_stamps.append(crplane['@DeltaT'])
            
            image_frame_nums.append(crplane['@TheT'])
        stim_events=doc['OME']['ROI']
        
        for crstim in stim_events:
            stim_times.append(crstim['Union']['Shape']['@theT'])

        return (time_stamps,image_frame_nums,stim_times)


def get_stim_depths(logfilein):
    
    with open(logfilein,'r') as log_file:
        write_flag=False
        elapsed_on_flag=False
        depths=[]
        times=[]
        for line in log_file:
            pieces=line.split()
            
            print(pieces[0])
            
            if pieces[0] == 'Elapsed':
                elapsed_on_flag=True
            elif elapsed_on_flag:
                write_flag=True
                elapsed_on_flag=False

            if write_flag:
                
                depths.append(pieces[28])
                times.append(pieces[0])

    return (depths,times)

def convert_stim_times(stim_times,frame_flag=False,offset=False,time_between_frames=.12642225):
    converted_times=[]
    converted_frames=[]
    for i in stim_times[1:]:
        if not frame_flag:
            vls=i.split(':')
            converted_times.append(float(vls[-1])+60*float(vls[-2]))
        else:
           crframe=int(i)-offset
           converted_frames.append(crframe)
           converted_times.append((crframe+1)*time_between_frames)
    return (converted_times,converted_frames)

def get_delta_f(mn_roi,stim_frames,preframes,postframes,pre_frame_buffer=0):
    u, ind = np.unique(stim_frames, return_index=True)
    sorted_frames=u[np.argsort(ind)]
    st={}
    st['sorted_frames']=sorted_frames
    st['pre_f']={}
    st['pst_f']={}
    for cr_roi_ind in np.arange(len(mn_roi)):
        st['pre_f'][cr_roi_ind]=[]
        st['pst_f'][cr_roi_ind]=[]
        

    
    for cr_roi_ind in np.arange(len(mn_roi)):
        for crframe in sorted_frames:
           
            st['pre_f'][cr_roi_ind].append(np.mean(np.array(mn_roi[cr_roi_ind])[crframe-preframes-pre_frame_buffer:crframe-pre_frame_buffer]))
            
            st['pst_f'][cr_roi_ind].append(np.mean(np.array(mn_roi[cr_roi_ind])[crframe+1:crframe+postframes+1]))
            
    return st

           
def get_stim_region(logfilein,unique_events=1):
    roi_collect_flag=False
    initflag=True
    xlist=[]
    ylist=[]
    xpixels=[]
    ypixels=[]
    with open(logfilein,'r') as log_file:
        for line in log_file:
            pieces=line.split()
            if pieces[2]=='events:':
                num_of_events=int(pieces[-1])
                break
                roi_collect_flag=False
        for line in log_file:
            pieces=line.split()

            
            if pieces[0]=='Event:':
                roi_collect_flag=False
                if not initflag:
                    
                    xlist.append(xpixels)
                    ylist.append(ypixels)
                    xpixels=[]
                    ypixels=[]

            if roi_collect_flag:
                initflag=False
                vls=pieces[0].split(',')
                xpixels.append(vls[0])

                try:
                    ypixels.append(vls[1])
                except:
                    pdb.set_trace()
            

            if len(pieces)>2:
                if pieces[2] == 'points:':
                    
                    roi_collect_flag=True
    log_file.close()
    
    xlist.append(xpixels)
    ylist.append(ypixels)
    
    xreturn_list=[]

    yreturn_list=[]

    for cr_event in np.arange(unique_events):
        xreturn_list.append([int(i) for i in xlist[cr_event]])
        yreturn_list.append([int(i) for i in ylist[cr_event]])
    
    return (xreturn_list,yreturn_list)
          

