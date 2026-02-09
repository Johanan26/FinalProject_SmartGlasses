import { useNavigate } from "react-router-dom";

export default function Ai_questions() { 
            const navigate = useNavigate();


    navigate("/ai_question", { replace: true })
    return (
        <div>
          <button className = "flex absolute top-0 left-0 text-white bg-gradient-to-r from-red-400 via-red-500 to-red-600 hover:bg-gradient-to-br focus:ring-red-300 dark:focus:ring-red-800 font-medium rounded text-sm px-4 py-2.5 text-center" 
                                onClick={() => navigate("/home")}>Back</button> 
        </div>
    );
 };