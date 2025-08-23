class ApiResponse{
    statusCode:number;
    data:any;
    message:string="Successfull";
    success:boolean;
    constructor(statusCode:number=200,data:unknown=null,message:string="Successfull",success:boolean=true){
        this.statusCode=statusCode,
        this.data=data,
        this.message=message,
        this.success=success,
        this.success=statusCode<400;


    }
}

export {ApiResponse}
