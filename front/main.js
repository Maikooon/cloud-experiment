import './style.css';
import 'bulma/css/bulma.css';
import { DefaultApi } from './api/index.ts';

const api = new DefaultApi();
api.uploadPost();

document.querySelector('#app').innerHTML = `
  <div>
    <h1>テスト</h1>
    <p>値の埋め込み例: 1 + 1 = ${1 + 1}</p>
  </div>
`;
