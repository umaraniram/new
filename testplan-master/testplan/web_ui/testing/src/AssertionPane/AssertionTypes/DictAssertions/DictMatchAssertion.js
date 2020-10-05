import React, {useState} from 'react';
import PropTypes from 'prop-types';
import DictBaseAssertion from './DictBaseAssertion';
import DictButtonGroup from './DictButtonGroup';
import DictCellRenderer from './DictCellRenderer';
import {
  prepareDictColumn,
  prepareDictRowData,
  sortFlattenedJSON,
} from './dictAssertionUtils';
import {SORT_TYPES} from '../../../Common/defaults';


/**
 * Component that renders DictMatch assertion.
 *
 * The expected dictionary   | The actual dictionary matched
 * of the test:              | to the expected one:
 *
 * {                         | {
 *   'foo': {                |   'foo': {
 *     'alpha': 'blue',      |     'alpha': 'red',
 *     'beta': 'green',      |     'beta': 'green',
 *   }                       |   }
 *   'bar': true             |   'bar': true
 * }                         | }
 *
 *  ______________________________________
 * | Key        | Expected   | Value      |
 * |------------|------------|------------|
 * | foo        |            |            |
 * |   alpha    | blue       | red        |
 * |   beta     | green      | green      |
 * | bar        | true       | true       |
 * |____________|____________|____________|
 *
 * The grid consists of three columns: Key, Expected and Value.
 *  - Key: a key of the dictionary. Nested objects are displayed with indented
 *    keys.
 *  - Expected: expected value for the given key. 
 *  - Value: Actual value for the given key.
 *
 */

export default function DictMatchAssertion(props) {
  const flattenedDict = sortFlattenedJSON(
    props.assertion.comparison, 0, false, true
  );
  const columns = prepareDictColumn(DictCellRenderer, true);

  const [rowData, setRowData] = useState(flattenedDict);
  
  const buttonGroup = (
    <DictButtonGroup
      sortTypeList={[
        SORT_TYPES.ALPHABETICAL,
        SORT_TYPES.REVERSE_ALPHABETICAL,
        SORT_TYPES.BY_STATUS,
        SORT_TYPES.ONLY_FAILURES
      ]}
      flattenedDict={flattenedDict}
      setRowData={setRowData}
      defaultSortType={SORT_TYPES.BY_STATUS}
    />
  );

  return (
    <DictBaseAssertion
      buttons={buttonGroup}
      columns={columns}
      rows={prepareDictRowData(rowData, props.assertion.line_no)}
    />
  );
}


DictMatchAssertion.propTypes = {
  /** Assertion being rendered */
  assertion: PropTypes.object.isRequired,
};
