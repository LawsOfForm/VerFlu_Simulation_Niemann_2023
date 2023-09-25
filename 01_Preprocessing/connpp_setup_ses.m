Author Filip Niemann, UMG Greifswald, 18.08.2021
% Sample CONN Script for the OSU Workshop
% Created by Andrew Jahn, University of Michigan, 02.27.2020
% Adapted from Alfonso Nieto-Castanon s script, www.alfnie.com


% FIND functional/structural files
% note: this will look for all data in these folders, irrespestive of the specific download subsets entered as command-line arguments

%define every task as separate session

NSUBJECTS=1;

cwd=data;  % get new directory from the located shell script

FileStruct_func = dir(fullfile(data,'**', '*task-categories*.nii'));
%struct to cell FUNCTIONAL_FILE.name
for i =1:length(FileStruct_func)
    FUNCTIONAL_FILE{i}=fullfile(FileStruct_func(i).folder,FileStruct_func(i).name);
end
%FUNCTIONAL_FILE=cellstr(conn_dir('task-categories*.nii')));

FileStruct_struc = dir(fullfile(data,'**', '*T1w.nii'));
%struct to cell FUNCTIONAL_FILE.name
for i =1:length(FileStruct_struc)
    STRUCTURAL_FILE{i}=fullfile(FileStruct_struc(i).folder,FileStruct_struc(i).name);
end


if rem(length(FUNCTIONAL_FILE),NSUBJECTS),error('mismatch number of functional files %n', length(FUNCTIONAL_FILE));end
if rem(length(STRUCTURAL_FILE),NSUBJECTS),error('mismatch number of anatomical files %n', length(FUNCTIONAL_FILE));end
nsessions=length(FUNCTIONAL_FILE)/(NSUBJECTS);
FUNCTIONAL_FILE=reshape(FUNCTIONAL_FILE,[nsessions, NSUBJECTS]);
STRUCTURAL_FILE={STRUCTURAL_FILE{1:NSUBJECTS}};
disp([num2str(size(FUNCTIONAL_FILE,1)),' sessions']);
disp([num2str(size(FUNCTIONAL_FILE,2)),' subjects']);

TR=5; % Repetition time  (virtuelle Repetition time 5 s, Timeaquisition 2 s)


% CONN-SPECIFIC SECTION: RUNS PREPROCESSING/SETUP/DENOISING/ANALYSIS STEPS
% Prepares batch structure
clear batch;
batch.filename=fullfile(cwd,'code','Preprocessing.mat');            % New conn_*.mat experiment name

% SETUP & PREPROCESSING step (using default values for most parameters, see help conn_batch to define non-default values)
% CONN Setup                                            % Default options (uses all ROIs in conn/rois/ directory); see conn_batch for additional options
% CONN Setup.preprocessing                               (realignment/coregistration/segmentation/normalization/smoothing)
batch.Setup.isnew=1;
batch.Setup.nsubjects=NSUBJECTS;
batch.Setup.RT=TR;                                        % TR (seconds)
batch.Setup.functionals=repmat({{}},[NSUBJECTS,1]);       % Point to functional volumes for each subject/session
for nsub=1:NSUBJECTS,for nses=1:nsessions,batch.Setup.functionals{nsub}{nses}{1}=FUNCTIONAL_FILE{nses,nsub}; end; end %note: each subject s data is defined by 2 sessions and one single (4d) file per session
batch.Setup.structurals=STRUCTURAL_FILE; % Point to anatomical volumes for each subject
%4 session with 2 conditions
nconditions=nsessions;                                  % treats each session as a different condition (comment the following three lines and lines 84-86 below if you do not wish to analyze between-session differences)
if nconditions==1
    batch.Setup.conditions.names={'Falsche_Vorverarbeitung'};
    for ncond=1,for nsub=1:NSUBJECTS,for nses=1:nsessions,              batch.Setup.conditions.onsets{ncond}{nsub}{nses}=0; batch.Setup.conditions.durations{ncond}{nsub}{nses}=inf;end;end;end     % rest condition (all sessions)
else
    batch.Setup.conditions.names=[{'Task'}, arrayfun(@(n)sprintf('Session%d',n),1:nconditions,'uni',0)];
    for ncond=1,for nsub=1:NSUBJECTS,for nses=1:nsessions,              batch.Setup.conditions.onsets{ncond}{nsub}{nses}=0; batch.Setup.conditions.durations{ncond}{nsub}{nses}=inf;end;end;end     % rest condition (all sessions)
    for ncond=1:nconditions,for nsub=1:NSUBJECTS,for nses=1:nsessions,  batch.Setup.conditions.onsets{1+ncond}{nsub}{nses}=[];batch.Setup.conditions.durations{1+ncond}{nsub}{nses}=[]; end;end;end
    for ncond=1:nconditions,for nsub=1:NSUBJECTS,for nses=ncond,        batch.Setup.conditions.onsets{1+ncond}{nsub}{nses}=0; batch.Setup.conditions.durations{1+ncond}{nsub}{nses}=inf;end;end;end % session-specific conditions
end
batch.Setup.preprocessing.steps={'functional_label_as_original','functional_realign','functional_center','functional_slicetime','structural_center','functional_segment&normalize_indirect','functional_label_as_mnispace','functional_smooth','functional_label_as_smoothed'};
batch.Setup.preprocessing.sliceorder='ascending';


%%Defaults at https://web.conn-toolbox.org/resources/conn_batch
batch.Setup.preprocessing.fwhm = 8;    

%%if EPI 155 remove first 5 scans
%batch.Setup.preprocessing.removescans = 5;

batch.Setup.done=1;
batch.Setup.overwrite='Yes';

conn_batch(batch); % runs Preprocessing and Setup steps only

%%
clear batch;
batch.filename=fullfile(cwd,'Vorverarbeitung_Test.mat');            % Existing conn_*.mat experiment name
