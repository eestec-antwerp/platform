import { parseAnalysisResult } from "../util"

class Job {
    constructor(token, company_name="", email="", file_name="", streaming=false) {
        this.token = token;
        this.company_name = company_name;
        this.email = email;
        this.file_name = file_name;
        this.streaming = streaming;
        this.progress = 0;
        this.result = undefined;
        this.outliers = [];

    }

    get done() {
        return this.progress == 100;
    }

    // Set the result for this job
    setResult(result) {
        this.result = parseAnalysisResult(result);
    }

    // Return the name for the column with the given index
    getNameFor(idx) {
        let column = this.result.fieldRecognition.filter(col => col.index == idx)[0];
        return column ? column.name : undefined;
    }

    update(new_job) {
        this.progress = new_job.progress;
        this.result = parseAnalysisResult(new_job.result);
    }
}

export default Job;
