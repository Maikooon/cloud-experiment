import './css/style.css';
import './css/header.css';
import './css/topImage.css';
import 'bulma/css/bulma.css';
import { DefaultApi } from './api/index.ts';

const api = new DefaultApi();
api.uploadPost();

document.querySelector('#app').innerHTML = `
  <div>
    <h1>テスト</h1>
    <p>ここにページを書きます</p>
  </div>
`;