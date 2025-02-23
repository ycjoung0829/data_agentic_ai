import React, { useState } from "react";
import { Button } from "@mui/material";

export default function FolderUpload() {
    const [files, setFiles] = useState([]);
    const [response, setResponse] = useState(null);
    const [status, setStatus] = useState("");

    const handleFolderChange = (event) => {
        setFiles(event.target.files);
    };

    const handleUpload = async () => {
        if (files.length === 0) {
            alert("Please select a folder first");
            return;
        }

        const formData = new FormData();
        formData.append("folder_name", files[0].webkitRelativePath.split('/')[0]);
        
        for (const file of files) {
            formData.append("folder", file);
        }

        try {
            const res = await fetch("http://localhost:8000/upload-folder/", {
                method: "POST",
                body: formData,
            });
            const data = await res.json();
            console.log(data);
            setResponse(data);
            setStatus("Folder upload completed");
        } catch (error) {
            console.error("Upload failed", error);
            setStatus("Error uploading folder");
        }
    };

    return (
        <div className="p-4 space-y-4">
            <h1 className="text-xl font-bold">Upload a Folder</h1>
            <h3>{status}</h3>
            <input type="file" webkitdirectory="" directory="" multiple onChange={handleFolderChange} className="border p-2" />
            <Button 
                onClick={handleUpload} 
                className="bg-blue-500 text-white px-4 py-2 rounded"
            >
                Upload Folder
            </Button>
            {response && (
                <div className="mt-4 p-2 border rounded">
                    <h2 className="font-bold">Response:</h2>
                    <pre className="bg-gray-100 p-2">{JSON.stringify(response, null, 2)}</pre>
                </div>
            )}
        </div>
    );
}