
# model_names_list, SU_NO, SUType,  binary_list_to_doad  base is calling start_download(['{model_names_list}'], {SU_NO}, '{SUType}', ['{SourceSoftware}'],)") oadStatus[id] = "INTERUPTED"


from api import startDownload


def notify(id, model_names_list, SU_NO, SUType, NEWSourceSoftware, OLDSofware, NEWEVT_TYPE):

    if NEWSourceSoftware != OLDSofware:
        print("Download Status updated")
        return {id: "Downloaded"} if startDownload(
            id, model_names_list, SU_NO, SUType, NEWSourceSoftware) == "0" else "Interupted"
    elif NEWEVT_TYPE == "Failed":
        print("Dear HOST Machine the job Failed.")
        print("Calling delete_submission()API")
    elif NEWEVT_TYPE == "PASSED":
        print("Dear HOST Machine the job PASSED.")
        print("Calling delete_submission()API")
