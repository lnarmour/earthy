from RiskInDroid import RiskInDroid
import os


apk_file = os.getenv('APK_FILE')

rid = RiskInDroid()

permissions = rid.get_permission_json(apk_file)

score = rid.calculate_risk(rid.get_feature_vector_from_json(permissions))

print('{},{}'.format(apk_file, score))
