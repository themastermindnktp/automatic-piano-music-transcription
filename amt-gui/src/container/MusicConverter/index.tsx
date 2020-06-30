import React, {useState} from 'react';
import {Button, Spin, Upload} from "antd";
import {UploadOutlined} from '@ant-design/icons';
import {UploadProps} from "antd/lib/upload/interface";
import { GetFileResultService, UploadFileService} from "../../services/musicConverter.service";
import './index.scss';
import HeaderPage from "./header";

const MusicConverter = () => {

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [response, setResponse] = useState<any>(null);
    const [fileList, setFileList] = useState<any[]>([]);

    const onChange = ({fileList}: any) => {
        setFileList(fileList);
    };

    const RequestGetFile = (midiFile: File) => {
        GetFileResultService(midiFile).then(data => setResponse(data)).catch(err => setResponse(null));
    }

    const uploadProps: UploadProps = {
        accept: 'audio/*',
        customRequest: ({file, onSuccess, onProgress}) => {
            setIsLoading(true);

            return UploadFileService(file).then((data: any) => {
                setResponse(data);
                setIsLoading(false);
                onSuccess(data, file);
                onProgress({percent: 100}, file);

                RequestGetFile(data.midiFile);
            }).catch(err => {
                setResponse(err);
                setIsLoading(false);
            });
        },
        style: {
            width: '50%'
        },
        listType: 'picture',
        onChange,
        // disabled: fileList.length > 0,
        progress: {
            strokeColor: {
                '0%': '#108ee9',
                '100%': '#87d068',
            },
            strokeWidth: 3,
            format: (percent: any) => `${parseFloat(percent.toFixed(2))}%`,
        },
    };

    return (
        <div>
            <HeaderPage buttonUpload={
                <Upload {...uploadProps}>
                    <Button disabled={fileList.length > 0}>
                        <p><UploadOutlined/> Upload File </p>
                    </Button>
                </Upload>
            }>

                <Spin spinning={isLoading}>
                    {
                        response && response.sheets ?
                            <div style={{textAlign: 'center', opacity: 0.6}}>
                                <h2> Sheet converted </h2>
                                {
                                    response && response.sheets ? response.sheets.map(
                                        (singleSheet: any) => {
                                            return <img src={singleSheet} alt={'this is sheets '}/>
                                        }
                                    ) : null
                                }
                            </div> : null
                    }
                </Spin>

            </HeaderPage>
        </div>
    );
}

export default MusicConverter;