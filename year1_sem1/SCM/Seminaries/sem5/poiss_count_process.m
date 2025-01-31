% Simulate a [0, Tmax] segment of a Poisson counting process.
clear all
lambda = input('frequency lambda = '); % given frequency
Tmax = input('time frame (in minutes) Tmax = '); % given time period
arr_times = -1/lambda * log(rand); % array containing arrival times
                                   % each interarriv. time is Exp(lambda)
last_arrival = arr_times;
while last_arrival <= Tmax
    last_arrival = last_arrival - 1/lambda * log(rand);
    arr_times = [arr_times, last_arrival];
end

arr_times = arr_times(1 : end - 1); % nr. of arrivals during time Tmax
% last last_arrival should not be included

%%% Graph the trajectory %%%
step = 0.01; % small step size, simulate continuity
t = 0 : step: Tmax; % time variable
Nsteps = length(t);
X = zeros(1, Nsteps); % Poisson process X(t)
for s = 1 : Nsteps
    X(s) = sum(arr_times <= t(s));
end % X(s) is the number of arrivals by the time t(s)
% X

% illustration
clf
axis([0 max(t) 0 max(X)]); hold on
title('Poisson process of arrivals')
xlabel('time'); ylabel('number of arrivals')
% plot(t, X, 'r')
comet(t, X);