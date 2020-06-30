import Axios from "axios";

const host = 'localhost:8080';
const uploadContext = '';

export const UploadFileService = (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    return Axios.post(`${host}${uploadContext}`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });

};

const hostMidiToSheet = 'https://solmire.com/miditosheetmusic/upload.php';

export const GetFileResultService = (file: File) => {
    const formData = new FormData();
    formData.append('midi', file);

    return Axios.post(`${hostMidiToSheet}`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};