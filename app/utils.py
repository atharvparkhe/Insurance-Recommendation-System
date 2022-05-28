




def matrix(ecg,carvasc,gluc):
    ohe = [[0,0,0],[0,0,1],[0,1,0],[1,0,0],[0,1,1],[1,0,1],[1,1,0],[1,1,1]]
    arr = [ecg,carvasc,gluc]
    return (ohe.index([arr])+1)*12.5