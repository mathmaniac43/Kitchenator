%Gesture=decision based on myo data
%1 = thumb to pinkie
%2 = fist
%3 = flex wrist
%4 = extend wrist
clc
mdl_cyton
Gesture=1;
ingredient=1

Tr = cyton.fkine(qr);
Tingred1 = SE3(.25,-.25,.15)*SE3.Rx(pi/2);
%qingred1 = cyton.ikine(Tingred1);
%Tingred2 = SE3(.10, -.25,.15)*SE3.Rx(pi/2);
%qingred2 = cyton.ikine(Tingred2);
%Tbowl = SE3(0.533,0.005,.8)*SE3.Rx(pi/2);
%Tpour = Tr*SE3.Rx(-pi/2);

t=[0:.1:2]';

if ingredient==1
    T1 = ctraj(Tr, Tingred1, 50);
    T2 = ctraj(Tingred1, Tr, 50);
else
    T1 = ctraj(Tr, Tingred2, 50);
    T2 = ctraj(Tingred2, Tr, 50);
end
q1 = cyton.ikine(T1);

q2 = flipud(q1);
qc = [q1; q2];
cyton.plot(qc)
%%

switch Gesture
    case 1
        %Thumb-to-pinkie = move to ingredient
        cyton.plot(q1)
        %send data to actual robot as well
    case 2
        %Fist = pick up ingredient
        %Need to figure out how to change the gripper
    case 3
        %Wrist flex = move to bowl
        %T1 = cyton.fkine(qingred1);
        %T2 = cyton.fkine(qr);
        %T = ctraj(T1, T2, 50);
        %q = cyton.ikine(T);
        %cyton.plot(q3)
    case 4
        %Wrist extend = pour ingredient and drop off ingredient
        %T = ctraj(Tr, Tpour, 50);
        %q = cyton.ikine(T);
        %cyton.plot(q)
end