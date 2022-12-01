% Detection of the minimum fluidization velocity Umf based on pressure vs.
% flowrate measurements acquired with the NI Daq and LabView. 
% The mass does not have to be entered anymore. p_0 is detected by taking
% the average value of the first 50 pressure readings. 

clear all;
close all;

%% Inputs-------------------------
nruns = 1; % [3 or 5] specify the number of experimental runs here
plim1 = 0.7; % [0.5] Lower bound for the fitting range. Usally 
plim2 = 0.9; % [0.8] Lower bound for the fitting range. Usally 
spread = 10;
% Optional inputs parameters
plotDensity = 4; %[2] Defines the number of datapoint in the plot. A higher number mean less points. 
max_flow = 200; % Maximum flow rate of the MFC in lpm
fillHeight = 0.30; % bed fill height [m]
nmbr_header_lines = 22; % [22] Number of lines in the datafile that are discarded. Set to a value larger than 22 if you have distrubing datapoint in the right part of the plot
max_flow = max_flow*spread; 
%---------------------------------------

%% Preallocation of memory
flow_lim = [1:max_flow];
nflow = size(flow_lim,2);
flow = zeros(nruns,nflow-1);
pdrops = zeros(nruns,nflow-1);
pdrops1 = zeros(nruns,100);
flow_rates1 = zeros(nruns,100);
countlim = 1 ;

%% Code Alexander Andres
%% Import file
filename = ['data_',num2str(1),'.lvm'];
delimiter = ',';
data = importdata(filename, delimiter, nmbr_header_lines);
%Take lenght and corresponding columns
alen = size(data.data(:,3));
flowdata(1:alen,1) = data.data(1:alen,3);
presdata(1:alen,1) = data.data(1:alen,5);

%% Calculation
%search for local min
TF = islocalmin(flowdata); 
half=23.6;
LH= flowdata < half;
TF= LH & TF;

%%
%See minimum on the plot
%x=1:length(flowdata);
%plot(x,flowdata,x(TF),flowdata(TF),'r*')

%% Minima and Maxima
%Find Minimums
Mins=find(TF == 1);
% 2nd Max
a= flowdata(Mins(1):Mins(2),:);
[M2,I2] =max(a(:));
max2=Mins(1)+I2;

%3rd Max
b=flowdata(Mins(2):length(flowdata),:);
[M3,I3] =max(b(:));
max3=Mins(2)+I3;

%Set the array and put together
flowdata1= flowdata(1:Mins(1));
flowdata2= flowdata(max2:Mins(2));
flowdata3= flowdata(max3:length(flowdata));
l1=length(flowdata1);
l2=length(flowdata2);
l3=length(flowdata3);
m= max([l1,l2,l3]);
flowf=NaN(m,3);
for k=1:l1
    flowf(k,1)=flowdata1(k);
end
for h=1:l2
    flowf(h,2)=flowdata2(h);
end
for d=1:l3
    flowf(d,3)=flowdata3(d);
end
%% Pressure
% Search for Maximum cause min are on the same spot as flow
c=presdata(Mins(1):Mins(2),:);
[M4,I4]= max(c(:));
pmax2 = Mins(1)+I4;
d=presdata(Mins(2):length(presdata),:);
[M5,I5]= max(d(:));
pmax3= Mins(2)+ I5;

%Plot to see the points
%x1=1:length(presdata);
%plot(x1,presdata,x1(TF),presdata(TF),'r*')

%Set the array and put together
presdata1= presdata(1:Mins(1));
presdata2= presdata(pmax2:Mins(2));
presdata3= presdata(pmax3:length(presdata));
l4=length(presdata1);
l5=length(presdata2);
l6=length(presdata3);
mp= max([l4,l5,l6]);
pres=NaN(mp,3);
for n=1:l4
    pres(n,1)=presdata1(n);
end
for v=1:l5
    pres(v,2)=presdata2(v);
end
for c=1:l6
    pres(c,3)=presdata3(c);
end

for i = 1:nruns
    %clear flow_rate pdrop
    %filename = ['data_',num2str(i),'.lvm'];
    %delimiter = ',';
    %data = importdata(filename, delimiter, nmbr_header_lines);
    szdata(i) = length(flowf(:,i));
    flow_rate(1:szdata(i))= flowf(1:szdata(i),i)*max_flow/100; 
    
    
    pdrop(1:szdata(i)) = pres(1:szdata(i),i); 
    p_0 = mean(pdrop(1:50));
    pdrop = pdrop/p_0;
    count = zeros(1,nflow-1);
 % Discretize data (Binning)   
    for k = 1:szdata(i)
        for m = 1:nflow-1
            if flow_rate(k)<=flow_lim(m+1)&&flow_rate(k)>flow_lim(m)
                count(m) = count(m)+1;
                flow(i,m) = flow(i,m)+flow_rate(k);
                pdrops(i,m) = pdrops(i,m)+pdrop(k);
                
            end
        end
    end
% %     
% Normalize by bin size
    for m = 1:nflow-1
        if count(m)<countlim
            flow(i,m) = 1/0;
            pdrops(i,m) = 1/0;
        else
            flow(i,m) = flow(i,m)/count(m);
            pdrops(i,m) = pdrops(i,m)/count(m);
        end
    end
    
    j=0;
    for m = 1:nflow-1
        if pdrops(i,m) > plim1 && pdrops(i,m) < plim2
            j = j+1;
            pdrops1(j) = pdrops(i,m);
            flow_rates1(j) = flow(i,m);
        end
    end
    flow_rates1(flow_rates1 == 0) = [];
    pdrops1(pdrops1 == 0) = [];
    
    flowMaxN(i) = max(flow_rate(:));
    
    
    x = transpose(flow_rates1(:));
    y = transpose(pdrops1(:));
    clear flow_rates1 pdrops1
    fit = polyfit(x,y,1);
    slope(i) = fit(1);
    intercept(i) = fit(2);
    clear x y fit flow_rate pdrop
    umf(i) = (1-intercept(i))/slope(i);
    %ustart(i) = (plim1-intercept(i))/slope(i);
    %ufinish(i) = (plim2-intercept(i))/slope(i);
end
flowMax = ceil(mean(flowMaxN));
umf=umf/spread;
umf_down = umf; 
umf_mean = mean(umf_down(1:nruns));
umf_std = std(umf_down(1:nruns));

disp(['-----------------------------'])
disp(['      Umf = ',num2str(round(umf_mean,1)),' ± ',num2str(round(umf_std,1)),' lpm'])
disp(['-----------------------------'])


%%
flow=flow./spread;
%%
if nruns == 3
figure(1)
plot(flow(1,1:plotDensity:end),pdrops(1,1:plotDensity:end),'k s','markersize',16,'linewidth',2),axis square
hold on
plot(flow(2,1:plotDensity:end),pdrops(2,1:plotDensity:end),'r o','markersize',16,'linewidth',2),axis square
plot(flow(3,1:plotDensity:end),pdrops(3,1:plotDensity:end),'g x','markersize',16,'linewidth',2),axis square
title(['U_{mf} = ', num2str(round(umf_mean,1)),' ','lpm'])
plot([0 flowMax*1.1],[1 1],'k -','linewidth',1)
plot([umf_mean umf_mean],[0 1],'k -','linewidth',1)
set(gca,'fontsize',16)
xlabel('Flow Rate (L/min)')
ylabel('\Delta P A_{bed} w^{-1}')
ylim([0 1.2])
xlim([0 flowMax*1.1/spread])
legend('Run1','Run2','Run3','location','eastoutside')
print('-djpeg','Umf_plot','-r300')


else
figure(1)
plot(flow(1,1:plotDensity:end),pdrops(1,1:plotDensity:end),'k s','markersize',16,'linewidth',2),axis square
hold on
plot(flow(2,1:plotDensity:end),pdrops(2,1:plotDensity:end),'r o','markersize',16,'linewidth',2),axis square
plot(flow(3,1:plotDensity:end),pdrops(3,1:plotDensity:end),'g x','markersize',16,'linewidth',2),axis square
plot(flow(4,1:plotDensity:end),pdrops(4,1:plotDensity:end),'b d','markersize',16,'linewidth',2),axis square
plot(flow(5,1:plotDensity:end),pdrops(5,1:plotDensity:end),'y +','markersize',16,'linewidth',2),axis square
title(['U_{mf} = ', num2str(round(umf_mean,1)),' ','lpm'])
plot([0 flowMax*1.1],[1 1],'k -','linewidth',1)
plot([umf_mean umf_mean],[0 1],'k -','linewidth',1)
set(gca,'fontsize',16)
xlabel('Flow Rate (L/min)')
ylabel('\Delta P A_{bed} w^{-1}')
ylim([0 1.2])
xlim([0 flowMax*1.1])
legend('Run1','Run2','Run3','Run4','Run5','location','eastoutside')
print('-djpeg','Umf_plot','-r300')
end
%%

% figure(2)
% 
% plot(flow(6,:),pdrops(6,:),'k s','markersize',16,'linewidth',2),axis square
% hold on
% plot(flow(7,:),pdrops(7,:),'r o','markersize',16,'linewidth',2),axis square
% plot(flow(8,:),pdrops(8,:),'g x','markersize',16,'linewidth',2),axis square
% plot(flow(9,:),pdrops(9,:),'b d','markersize',16,'linewidth',2),axis square
% plot(flow(10,:),pdrops(10,:),'y +','markersize',16,'linewidth',2),axis square
% plot([0 200],[1 1],'k -','linewidth',2)
% plot([umf_Zirc0405 umf_Zirc0405],[0 1],'k -','linewidth',2)
% set(gca,'fontsize',20)
% xlabel('Flow Rate (L/min)')
% ylabel('\Delta P A_{bed} w^{-1}')
% ylim([0 1.2])
% xlim([0 60])
% % legend('Dry','0.2 wt%','0.6 wt%','1.2 wt%','location','eastoutside')
% legend('run1','run2','run3','run4','run5','location','eastoutside')
% box on
% print('-dtiff','Zirconia 04-05')
% 
% figure(3)
% plot(flow(11,:),pdrops(11,:),'k s','markersize',16,'linewidth',2),axis square
% hold on
% plot(flow(12,:),pdrops(12,:),'r o','markersize',16,'linewidth',2),axis square
% plot(flow(13,:),pdrops(13,:),'g x','markersize',16,'linewidth',2),axis square
% plot(flow(14,:),pdrops(14,:),'b d','markersize',16,'linewidth',2),axis square
% plot(flow(15,:),pdrops(15,:),'y +','markersize',16,'linewidth',2),axis square
% plot([0 200],[1 1],'k -','linewidth',2)
% plot([umf_Zirc0405 umf_Zirc0405],[0 1],'k -','linewidth',2)
% set(gca,'fontsize',20)
% xlabel('Flow Rate (L/min)')
% ylabel('\Delta P A_{bed}
% w^{-1}')0..................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
% ylim([0 1.2])
% xlim([0 60])
% % legend('Dry','0.2 wt%','0.6 wt%','1.2 wt%','location','eastoutside')
% legend('run1','run2','run3','run4','run5','location','eastoutside')
% box on
% print('-dtiff','small Zircona beads')
% 
% flow_Glass05075 = mean(flow(1:5,:),1);
% flow_Zirc0405 = mean(flow(6:10,:),1);
% flow_Glass05070 = mean(flow(11:15,:),1);
% flow_Zirc0405 = mean(flow(16:20,:),1);
% 
% pdrops_Glass05075 = mean(pdrops(1:5,:),1);
% pdrops_Zirc0405 = mean(pdrops(6:10,:),1);
% pdrops_Glass05070 = mean(pdrops(11:15,:),1);
% pdrops_Zirc0405 = mean(pdrops(16:20,:),1);
% %%
% figure(5)
% plot(flow_Glass05075(:),pdrops_Glass05075(:),'k s','markersize',16,'linewidth',2),axis square
% hold on
% plot(flow_Zirc0405(:),pdrops_Zirc0405(:),'r o','markersize',16,'linewidth',2),axis square
% plot([umf_Zirc0405 umf_Zirc0405],[0 1],'k -','linewidth',2)
% plot([umf_Glass05075 umf_Glass05075],[0 1],'k -','linewidth',2)
% plot([0 200],[1 1],'k -','linewidth',2)
% 
% set(gca,'fontsize',20)
% xlabel('Flow Rate (L/min)')
% ylabel('\Delta P A_{bed} w^{-1}')
% ylim([0 1.2])
% xlim([0 60])
% % legend('Dry','0.2 wt%','0.6 wt%','1.2 wt%','location','eastoutside')
% legend('Glass 0.5 - 0.75 mm','Zirconia 0.4 - 0.6 mm','location','eastoutside')
% box on
% print('-dtiff','Small beads')