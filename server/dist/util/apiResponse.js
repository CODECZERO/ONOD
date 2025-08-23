class ApiResponse {
    constructor(statusCode = 200, data = null, message = "Successfull", success = true) {
        this.message = "Successfull";
        this.statusCode = statusCode,
            this.data = data,
            this.message = message,
            this.success = success,
            this.success = statusCode < 400;
    }
}
export { ApiResponse };
