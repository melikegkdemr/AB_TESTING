######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.


#####################################################
# Veriyi Hazırlama ve Analiz Etme
#####################################################

import pandas as pd
from scipy.stats import shapiro,levene,ttest_ind

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

control_group = pd.read_excel(r"ab_testing.xlsx",sheet_name="Control Group")
test_group = pd.read_excel(r"ab_testing.xlsx",sheet_name="Test Group")

control_group.head()
test_group.head()

def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)
    print("##################### Describes #####################")
    print(dataframe.describe().T)

check_df(control_group)
check_df(test_group)

control_group["Purchase"].mean()
test_group["Purchase"].mean()

#####################################################
# A/B Testinin Hipotezinin Tanımlanması
#####################################################

# h0: M1 = M2 (averagebidding ve maximumbidding teklif verme türlerinin dönüşüm getirileri arasında istatistiksel olarak anlamlı bir fark yoktur)
# h1: M1 != M2 (... vardır.)

control_group["Purchase"].mean()
test_group["Purchase"].mean()

#####################################################
# Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# Normallik Varsayımı

# h0: normal dağılım varsayımı sağlanmaktadır.
# h1: sağlanmamaktadır.

test_stat, pvalue = shapiro(control_group["Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

# kontrol grubu için p value > 0.05 --> h0 reddedilemez

test_stat, pvalue = shapiro(test_group["Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

# test grubu için p value > 0.05 --> h0 reddedilemez

# sonuç: normal dağılım varsayımı sağlanmaktadır.

# Varyans Homojenliği

# h0: varyanslar homojendir
# h1: varyanslar homojen değildir.

test_stat, pvalue = levene(control_group["Purchase"],
                           test_group["Purchase"])
print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))

# p value > 0.05 --> h0 reddedilemez

# sonuç: varyanslar homojendir


test_stat, pvalue = ttest_ind(control_group["Purchase"],
                           test_group["Purchase"], equal_var=True)

print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))


# p value > 0.05 --> h0 reddedilemez.
# sonuç: M1 = M2 (averagebidding ve maximumbidding teklif verme türlerinin dönüşüm getirileri arasında istatistiksel olarak anlamlı bir fark yoktur)
