from data.dashboard_data_model import DashboardDataModel
from data.result_data_model import ResultDataModel
from sqlite3_database.db_result import SqliteDbResult
from sqlite3_database.db_resume import SqliteDbResume
from sqlite3_database.db_jd import SqliteDbJD
import json

class ResultRepository:
    def __init__(self, dbResult: SqliteDbResult, dbResume: SqliteDbResume, dbJd: SqliteDbJD):
        self.dbResult = dbResult
        self.dbResume = dbResume
        self.dbJd = dbJd

    def fetchTotalCount(self) -> int:
        return self.dbResult.totalCount()

    def findMatchingResumesCount(self, jdId: int) -> int:
        return self.dbResult.totalMatchingResumesCount(jdId)

    def fetchMatchedResumeIds(self, jdId: int) -> list[int]:
        return self.dbResult.fetchMatchedResumeIds(jdId)

    def fetchDistinctResumeIds(self) -> list[int]:
        return self.dbResult.fetchAnalyzedResumeIds()

    def dropResultTables(self) -> None:
        self.dbResult.dropResultTables()

    def deleteAllResults(self) -> None:
        self.dbResult.deleteAllResults()

    def fetchResumeDetailsFromIds(self, resumeId: int, jdId: int) -> ResultDataModel:
        rows = self.dbResult.fetchDetailsFromIds(resume_id=resumeId, jd_id=jdId)
        data_model: ResultDataModel = ResultDataModel()
        for row in rows:
            data_model.resumeId = resumeId
            data_model.jdId = jdId
            data_model.matchingSkills = json.loads(row[3])
            data_model.matchPercent = int(row[4])
            data_model.missingSkills = json.loads(row[5])
            data_model.recommendation = row[6]
            data_model.strengths = row[7]
            data_model.weakness = row[8]
        return data_model

    def sortBy(self, data_model_list: list[DashboardDataModel], sort_by: str, order: str, sort_array: list[str], order_array: list[str]) -> None:
        reverse_order = True if order == order_array[0] else False
        if sort_by == sort_array[0]:
            data_model_list.sort(key=lambda x: int(x.matchPercent), reverse=reverse_order)
        elif sort_by == sort_array[1]:
            data_model_list.sort(key=lambda x: float(x.experience.split()[0]), reverse=reverse_order)

    def fetchTopNResults(self, n: int, jdId: int) -> list[DashboardDataModel]:
        if jdId > -1:
            rows = self.dbResult.fetchTopNResultsForJdId(n, jdId)
        else:
            rows = self.dbResult.fetchTopNResults(n)
        resultList = []
        for rankCounter, row in enumerate(rows, start=1):
            name = self.dbResume.fetchNameFromId(row[2])
            experience = f"{self.dbResume.fetchExpFromId(row[2])} years"
            totalReqSkillsCount = self.dbJd.fetchTotalSkillsCount(row[1])
            matchedSkills = len(json.loads(row[3]))
            resultList.append(
                DashboardDataModel(rank=f"{rankCounter}", name=name,
                                   experience=experience, matchPercent=f"{int(row[4])}", 
                                   skills_matched=f"{matchedSkills}/{totalReqSkillsCount}",
                                   resume_id= row[2], jd_id= row[1]))
        return resultList
        
