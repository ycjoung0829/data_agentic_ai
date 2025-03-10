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
        formData.append("folder_name", files[0].webkitRelativePath.split("/")[0]);

        Array.from(files).forEach((file) => {
            formData.append("folder", file);
        });

        try {
            const res = await fetch("http://localhost:8000/upload-folder/", {
                method: "POST",
                body: formData,
            });
            const data = await res.json();
            setResponse(data);
            setStatus("✅ Folder upload completed");
        } catch (error) {
            console.error("Upload failed", error);
            setStatus("❌ Error uploading folder");
        }
    };

    return (
        <div className="p-6 space-y-6 max-w-lg mx-auto bg-white shadow-lg rounded-lg">
            <h1 className="text-2xl font-bold text-center text-gray-700">📂 Upload a Folder</h1>
            <p className="text-center text-gray-500">Select a folder and upload it to the server.</p>
            <h3 className={`text-center font-semibold ${status.includes('Error') ? 'text-red-500' : 'text-green-500'}`}>{status}</h3>
            <div className="flex justify-center">
                <input 
                    type="file" 
                    webkitdirectory="" 
                    directory="" 
                    multiple 
                    onChange={handleFolderChange} 
                    className="border p-2 rounded-md cursor-pointer file:hidden"
                />
            </div>
            <div className="flex justify-center">
                <Button 
                    onClick={handleUpload} 
                    variant="contained" 
                    color="primary"
                    className="w-full py-2"
                >
                    🚀 Upload Folder
                </Button>
            </div>
            {response && (
                <div className="mt-6 p-4 border rounded bg-gray-100">
                    <h2 className="font-bold text-gray-700">📝 Response:</h2>
                    <pre className="bg-white p-2 overflow-auto rounded-md border border-gray-300">
                        {JSON.stringify(response, null, 2)}
                    </pre>
                </div>
            )}
        </div>
    );
}