import csv, matplotlib.pyplot as plt, numpy as np, pandas as pd, scipy

dates = ['2018/01/11', '2017/12/24', '2017/12/26', '2018/01/10', '2017/12/22', '2017/12/23', '2017/12/25']

def cvt_time(t):
    h, m, s = t[0], t[1], t[2]
    if h<6: return 1
    if h<9: return 2
    if h<12: return 3
    if h<14: return 4
    if h<17: return 5
    if h<19: return 6
    if h<22: return 7
    return 8
    # _[2]+_[1]*60+_[0]*3600 

def load_data(path):    
    with open(path, 'r') as f:
        data = []
        reader = csv.DictReader(f)
        for line in reader:
            line['Date'] = dates.index(line['Date'])
            line['Time'] = [cvt_time(_) for _ in [list(map(int,line['Time'].split(':')))]][0]
            for key in line:
                if key!="Date" and key!="Time":
                    line[key]=float(line[key])
            if line['Room_Occupancy_Count']>0:
                data.append(line)
            #print(line)
        return data
        
raw_data = load_data('Occupancy_Estimation.csv')

label_to_index = {}
labels = []
for key in raw_data[0]: label_to_index[key] = len(label_to_index); labels.append(key)

print(label_to_index)
print(set(map(lambda x:x['Date'], raw_data)))

def cov(x, y): return np.mean((x-np.mean(x))*(y-np.mean(y))) # E((X-u_x)(Y-u_y))
def std(x): return np.std(x)

def select_by_key(key): 
    def f(it): return it[key]
    return f

def correlation_coeff(data, selector1, selector2):
    x = list(map(selector1, data))
    y = list(map(selector2, data))    
    pearson_coeff = cov(x,y) / (std(x)*std(y))
    return pearson_coeff
    

correlation_coeff(raw_data, select_by_key("S1_Temp"), select_by_key("S2_Temp"))

def panda_corr():
    data=[]
    for d in raw_data:
        l = np.zeros((len(labels),))
        for k in d.keys(): 
            if not isinstance(d[k], str): l[label_to_index[k]]=d[k]
        data.append(l)
    data = np.array(data)

    df = pd.DataFrame(data, columns=labels)
    print(df.corr())
    print(data.shape)
    

def correlation_matrix(data, labels, label_to_index):
    M = np.zeros((len(labels), len(labels)))
    for i in range(len(labels)):
        for j in range(i+1, len(labels)):
            if not isinstance(data[0][labels[i]], str) and not isinstance(data[0][labels[j]], str):
                M[j,i] = correlation_coeff(data, select_by_key(labels[i]), select_by_key(labels[j]))
    return M

def plot_mat(M, labels, export_file):
    fig = plt.figure(figsize=(10, 6), dpi=80)
    ax = fig.add_subplot(111)    

    cax = ax.matshow(M, cmap='plasma', interpolation='nearest')
    fig.colorbar(cax)
    for (i, j), z in np.ndenumerate(M):
        ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center', size=8)
        
    xaxis = np.arange(len(labels))
    ax.set_xticks(xaxis)
    ax.set_yticks(xaxis)
    #ax.xticks(rotation=90)

    ax.set_xticklabels(labels, rotation=90, size=8)
    ax.set_yticklabels(labels, size=8)
    ax.axis('image')    
    plt.savefig(export_file)    
    plt.close()
    

cor_mat = correlation_matrix(raw_data, labels, label_to_index); plot_mat(cor_mat, labels, "cor_mat.png")

def chi2_test(data, selector1, selector2):
    x = list(map(selector1, data))
    y = list(map(selector2, data))
    
    
    kx = list(map(lambda t:int(t), x))
    ky = list(map(lambda t:int(t), y))
    
    classes_x = list(set(kx))
    classes_y = list(set(ky))
    
    M = np.zeros((len(classes_x), len(classes_y)))
    for i in range(len(kx)):
        mx = classes_x.index(kx[i])
        my = classes_y.index(ky[i])
        M[mx,my]+=1
    
    return scipy.stats.chi2_contingency(M).pvalue
    
    R_tot = np.sum(M, axis=1)
    C_tot = np.sum(M, axis=0)    
    T = np.sum(M) 
    
    E = R_tot.reshape((-1, 1))*C_tot.reshape((1,-1))/T    
        
    X2 = np.sum(np.square(M-E)/E)    
    print(X2)
    
    deg_freedom = (len(R_tot)-1)*(len(C_tot)-1)
    
    return 1-scipy.stats.chi2.cdf(X2, deg_freedom)
    
def indep_matrix(data, labels, label_to_index):
    M = np.zeros((len(labels), len(labels)))
    for i in range(len(labels)):
        for j in range(len(labels)):
            if not isinstance(data[0][labels[i]], str) and not isinstance(data[0][labels[j]], str):
                M[j,i] = chi2_test(data, select_by_key(labels[i]), select_by_key(labels[j]))
    return M
    
ind_mat = indep_matrix(raw_data, labels, label_to_index); plot_mat(ind_mat, labels, "ind_mat.png")
    
def to_xy(raw_data, y_label):
    data=[]
    for d in raw_data:
        l = np.zeros((len(labels),))
        for k in d.keys(): 
            if not isinstance(d[k], str): l[label_to_index[k]]=d[k]
        data.append(l)
    data = np.array(data)    
    y_col =label_to_index[y_label]
    y = data[:, y_col]
    x = np.concatenate([data[:, :y_col], data[:,y_col+1:]], axis=1)
    return x, y.reshape((-1, 1))
    
    
    
def lsm(raw_data):
    x, y = to_xy(raw_data, "Room_Occupancy_Count")
    x_t = np.transpose(x)
    b = np.matmul(np.matmul(np.linalg.inv(np.matmul(x_t, x)), x_t), y)
    return b


b = lsm(raw_data)
print(b)

def plot_importance():
    fig = plt.figure(figsize=(10, 6), dpi=80)
    ax = fig.add_subplot(111)    
    ax.bar(labels[:-1], (b.reshape((-1,))))
    ax.set_xticklabels(labels[:-1],rotation=90, size=8)
    #plt.show()
    plt.savefig("feat_importance.png")
    
plot_importance()
    
def plot_date():
    x, y = to_xy(raw_data, "Time")
    print(y)
    fig = plt.figure(figsize=(10, 6), dpi=80)
    ax = fig.add_subplot(111)    
    plt.hist(y)
    #ax.set_xticklabels(dates,rotation=0, size=8)
    plt.savefig("time.png")    

plot_date()