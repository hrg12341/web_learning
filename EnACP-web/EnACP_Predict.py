#-*- coding: UTF-8 -*-
import lightgbm as lgb
import sys
import glob
import pandas as pd
import os
from sklearn.externals import joblib



def main(argv):

#   Feature extraction

    filepath = argv[1]
    datapath,filename = os.path.split(filepath)
    feature_dir = "Input_data/Input_data_feature"+"/"+filename+"/"
    mkd(feature_dir)
    extracts(filepath, feature_dir)

#   Loading feature

    feature_file = glob.glob(feature_dir+'/*')
    data_List = datadic(feature_file)
    data = trainmodel_GBM(data_List)

#   Loading model

    SVM_path="model/SVM_model/"
    model = joblib.load(SVM_path+"SVM_model.pkl")

#   Prediction

    result = model.predict_proba(data)

#   Storing the result
    result = pd.DataFrame(columns=["Non-ACP","ACP"],data=result)

    result.to_csv("../"+datapath+"/Output/"+filename+".csv")
    print(result)



def datadic(feature_file):

    method = ["feature-CC.csv","feature-DT.csv","-PDT-Profile.csv","-Top-n-gram.csv","-PSSM-RT.csv","-PSSM-DT.csv","-CC-PSSM.csv","-AC-PSSM.csv","ACC-PSSM.csv","kmer","feature-AC.csv","ACC.csv","DP.csv","DR.csv","PC-PseAAC.csv","PC-PseAAC-General.csv","PDT.csv","SC-PseAAC.csv","SC-PseAAC-General.csv"]
    featureDic={}
    for methodname in method:
        for i in feature_file:
            if methodname in i:
                featureDic[methodname]=i
                break

    for feature_name in featureDic:
        feature_path=featureDic[feature_name]

        dataset = pd.read_csv(feature_path,header=None,low_memory=False)
        dataset = dataset.convert_objects(convert_numeric=True)
        dataset.dropna(inplace = True)
        featureDic[feature_name]=dataset

    return featureDic


def trainmodel_GBM(datadic):

    test_feature  = {}
    for feature_name in datadic:
        y_pred = lightgbmTrainStag(datadic[feature_name],feature_name)
        test_feature[feature_name]=y_pred
    test_feature_vector  = pd.DataFrame(test_feature)
    new_Feature = test_feature_vector.values

    return new_Feature

def extracts(filepath,drec):
    drec = "../"+drec
    filepath="../"+filepath

    fname,filename = os.path.split(filepath)
    os.chdir("../EnACP-master/BioSeq-Analysis")
    #print("fanme",fname)
    print (filepath)
    print (drec)
    mkd(fname+'/Input_Features')
    mkd(fname + '/Ouput')
    feature_path=fname+'/Input_Features/'

    # nac.pyc 3 methods
    if (not os.path.exists(feature_path + filename + "_feature-kmer.csv")):
        print("Kmer method")
        os.system("python      nac.pyc " + filepath + " Protein Kmer -out " + feature_path + filename + "_feature-kmer.csv -f csv")
    else:
        pass

    if (not os.path.exists(feature_path + filename + "_feature-DR.csv")):
        print("DR method")
        os.system("python      nac.pyc " + filepath + " Protein DR -out " + feature_path + filename + "_feature-DR.csv -f csv")
    else:
        pass

    if (not os.path.exists(feature_path + filename + "_feature-DP.csv")):
        print("DP method")
        os.system("python      nac.pyc " + filepath + " Protein DP  -out " + feature_path + filename + "_feature-DP.csv -f csv")
    else:
        pass

    # acc.pyc 8 methods
    if (not os.path.exists(feature_path + filename + "_feature-AC.csv")):
        print("AC")
        os.system("python    acc.pyc " + filepath + " Protein AC -out " + feature_path + filename + "_feature-AC.csv -f csv")
    else:
        pass

    if (not os.path.exists(feature_path + filename + "_feature-CC.csv")):
        print("CC")
        os.system("python   acc.pyc " + filepath + " Protein CC -out " + feature_path + filename + "_feature-CC.csv -f csv")
    else:
        pass

    if (not os.path.exists(feature_path + filename + "_feature-ACC.csv")):

        print("ACC")
        os.system("python    acc.pyc " + filepath + " Protein ACC -out " + feature_path + filename + "_feature-ACC.csv -f csv")
    else:
        pass

    if (not os.path.exists(feature_path + filename + "_feature-PDT.csv")):

        print("PDT")
        os.system("python      acc.pyc " + filepath + " Protein PDT -out " + feature_path + filename + "_feature-PDT.csv -f csv")
    else:
        pass

    if (not os.path.exists(feature_path + filename + "_feature-PC-PseAAC.csv")):

        print("PC-PseAAC")
        os.system(
            "python      pse.pyc " + filepath + " Protein PC-PseAAC -out " + feature_path + filename + "_feature-PC-PseAAC.csv -f csv")
    else:
        pass

    if (not os.path.exists(feature_path + filename + "_feature-SC-PseAAC.csv")):

        print("SC-PseAAC")
        os.system(
            "python      pse.pyc " + filepath + " Protein SC-PseAAC -out " + feature_path + filename + "_feature-SC-PseAAC.csv -f csv")
    else:
        pass

    if (not os.path.exists(feature_path + filename + "_feature-PC-PseAAC-General.csv")):

        print("PC-PseAAC-General")
        os.system(
            "python      pse.pyc " + filepath + " Protein PC-PseAAC-General -out " + feature_path + filename + "_feature-PC-PseAAC-General.csv -f csv")
    else:
        pass

    if (not os.path.exists(feature_path + filename + "_feature-SC-PseAAC-General.csv")):

        print("SC-PseAAC-General")
        os.system(
            "python      pse.pyc " + filepath + " Protein SC-PseAAC-General -out " + feature_path + filename + "_feature-SC-PseAAC-General.csv -f csv")
    else:
        pass
    #profile.pyc 9 methods

    if (not os.path.exists(feature_path + filename + "_feature-AC-PSSM.csv")):
        print("AC-PSSM ")
        os.system(
            "python      profile.pyc " + filepath + " AC-PSSM -out " + feature_path + filename + "_feature-AC-PSSM.csv -f csv")
    else:
        pass
        #print(filename, "AC-PSSM method has existed")

    if (not os.path.exists(feature_path+ filename + "_feature-Top-n-gram.csv")):
        print("Top-n-gram")
        os.system(
            "python profile.pyc " + filepath + " Top-n-gram -out " + feature_path + filename + "_feature-Top-n-gram.csv -f csv -n 2")
    else:
        pass
        #print(filename, "Top-n-gram method has existed")

    if (not os.path.exists(feature_path + filename + "_feature-PDT-Profile.csv")):
        print("PDT-Profile")
        os.system(
            "python profile.pyc " + filepath + " PDT-Profile -out " + feature_path + filename + "_feature-PDT-Profile.csv -f csv -n 2")
    else:
        pass
        #print(filename, "PDT-Pofile method has existed")

    if (not os.path.exists(feature_path + filename + "_feature-CC-PSSM.csv")):

        print("CC-PSSM")
        os.system(
            "python profile.pyc " + filepath + " CC-PSSM -out " + feature_path + filename + "_feature-CC-PSSM.csv -f csv")
    else:
        pass
        #print(filename, "CC-PSSM method has existed")

    if (not os.path.exists(feature_path + filename + "_feature-ACC-PSSM.csv")):
        print("ACC-PSSM")
        os.system(
            "python profile.pyc " + filepath + " ACC-PSSM -out " + feature_path + filename + "_feature-ACC-PSSM.csv -f csv ")
    else:
        pass
        #print(filename, "ACC-PSSM method has existed")

    if (not os.path.exists(feature_path + filename + "_feature-PSSM-DT.csv")):
        print("PSSM-DT")
        os.system(
            "python profile.pyc " + filepath + " PSSM-DT -out " + feature_path + filename + "_feature-PSSM-DT.csv -f csv")
    else:
        pass
        #print(filename, "PSSM-DT method has existed")

    if (not os.path.exists(feature_path + filename + "_feature-PSSM-RT.csv")):
        print("PSSM-RT")
        os.system(
            "python profile.pyc " + filepath + " PSSM-RT  -out " + feature_path + filename + "_feature-PSSM-RT.csv -f csv ")
    else:
        pass
        #print(filename, "PSSM-RT method has existed")

    if (not os.path.exists(feature_path + filename + "_feature-DT.csv")):
        print("DT")
        os.system("python profile.pyc " + filepath + " DT -out " + feature_path + filename + "_feature-DT.csv -f csv ")
    else:
        pass
    os.chdir("../")

def mkd(x):

    if(os.path.exists(x)):
        pass
    else:
        os.makedirs(x)

def lightgbmTrainStag(data,featurename):
    model_path="model/lightgbm_model/"
    clf = lgb.Booster(model_file=model_path+'lightgbm_model'+featurename+'.txt')
    y_pred=clf.predict(data,num_iteration=clf.best_iteration,predict_disable_shape_check=True)

    return y_pred

if __name__ == '__main__':
	main(sys.argv)