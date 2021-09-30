## Containers

```js noeditor
import styles from './../src/components/shared/Panel/Panel.module.scss';
import Panel from './../src/components/shared/Panel/Panel';

<>
    <Panel styleName={styles.Panel}>
        This is a panel to hold UI elements
    </Panel>
    <Panel styleNames={styles.Panel}>
        This is a panel with a nested panel
        <Panel styleNames={styles.Panel}>
            This is a nested panel
        </Panel>
    </Panel>
</>
```