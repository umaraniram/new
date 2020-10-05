import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {css} from 'aphrodite';
import {
  Button,
  Collapse,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  Input,
  Label,
  Navbar,
  Nav,
  NavItem,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  UncontrolledDropdown,
  Table
} from 'reactstrap';

import FilterBox from "../Toolbar/FilterBox";
import {STATUS, STATUS_CATEGORY} from "../Common/defaults";

import {library} from '@fortawesome/fontawesome-svg-core';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';

import {
  faInfo,
  faBook,
  faPrint,
  faFilter,
  faTags,
  faQuestionCircle,
} from '@fortawesome/free-solid-svg-icons';

import styles from "./navStyles";


library.add(
  faInfo,
  faBook,
  faPrint,
  faFilter,
  faTags,
  faQuestionCircle,
);


/**
 * Toolbar component, contains the toolbar buttons & Filter box.
 */
class Toolbar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      helpModal: false,
      filterOpen: false,
      infoModal: false,
      filter: 'all',
      displayEmpty: true,
      displayTags: false,
    };

    this.filterOnClick = this.filterOnClick.bind(this);
    this.toggleInfoOnClick = this.toggleInfoOnClick.bind(this);
    this.toggleEmptyDisplay = this.toggleEmptyDisplay.bind(this);
    this.toggleHelpOnClick = this.toggleHelpOnClick.bind(this);
    this.toggleTagsDisplay = this.toggleTagsDisplay.bind(this);
    this.toggleFilterOnClick = this.toggleFilterOnClick.bind(this);
  }

  toggleHelpOnClick() {
    this.setState(prevState => ({
      helpModal: !prevState.helpModal
    }));
  }

  toggleInfoOnClick() {
    this.setState(prevState => ({
      infoModal: !prevState.infoModal
    }));
  }

  toggleFilterOnClick() {
    this.setState(prevState => ({
      filterOpen: !prevState.filterOpen
    }));
  }

  filterOnClick(e){
    let checkedValue = e.currentTarget.value;
    this.setState({filter: checkedValue});
    this.props.updateFilterFunc(checkedValue);
  }

  toggleEmptyDisplay() {
    this.props.updateEmptyDisplayFunc(!this.state.displayEmpty);
    this.setState(prevState => ({
      displayEmpty: !prevState.displayEmpty
    }));
  }

  toggleTagsDisplay() {
    this.props.updateTagsDisplayFunc(!this.state.displayTags);
    this.setState(prevState => ({
      displayTags: !prevState.displayTags
    }));
  }

  /**
   * Return the info button which toggles the info modal.
   */
  infoButton() {
    return (
      <NavItem>
        <div className={css(styles.buttonsBar)}>
          <FontAwesomeIcon
            key='toolbar-info'
            className={css(styles.toolbarButton)}
            icon='info'
            title='Info'
            onClick={this.toggleInfoOnClick}
          />
        </div>
      </NavItem>
    );
  }

  /**
   * Return the filter button which opens a drop-down menu.
   */
  filterButton(toolbarStyle) {
    return (
      <UncontrolledDropdown nav inNavbar>
        <div className={css(styles.buttonsBar)}>
          <DropdownToggle nav className={toolbarStyle}>
            <FontAwesomeIcon
              key='toolbar-filter'
              icon='filter'
              title='Choose filter'
              className={css(styles.toolbarButton)}
            />
          </DropdownToggle>
        </div>
        <DropdownMenu className={css(styles.filterDropdown)}>
          <DropdownItem toggle={false}
            className={css(styles.dropdownItem)}>
            <Label check className={css(styles.filterLabel)}>
              <Input type="radio" name="filter" value='all'
                checked={this.state.filter === 'all'}
                onChange={this.filterOnClick}/>{' '}
              All
            </Label>
          </DropdownItem>
          <DropdownItem toggle={false}
            className={css(styles.dropdownItem)}>
            <Label check className={css(styles.filterLabel)}>
              <Input type="radio" name="filter" value='fail'
                checked={this.state.filter === 'fail'}
                onChange={this.filterOnClick}/>{' '}
              Failed only
            </Label>
          </DropdownItem>
          <DropdownItem toggle={false}
            className={css(styles.dropdownItem)}>
            <Label check className={css(styles.filterLabel)}>
              <Input type="radio" name="filter" value='pass'
                checked={this.state.filter === 'pass'}
                onChange={this.filterOnClick}/>{' '}
              Passed only
            </Label>
          </DropdownItem>
          <DropdownItem divider />
          <DropdownItem toggle={false}
            className={css(styles.dropdownItem)}>
            <Label check className={css(styles.filterLabel)}>
              <Input type="checkbox" name="displayEmptyTest"
                checked={!this.state.displayEmpty}
                onChange={this.toggleEmptyDisplay}/>{' '}
              Hide empty testcase
            </Label>
          </DropdownItem>
        </DropdownMenu>
      </UncontrolledDropdown>
    );
  }

  /**
   * Return the button which prints the current testplan.
   */
  printButton() {
    return (
      <NavItem>
        <div className={css(styles.buttonsBar)}>
          <FontAwesomeIcon
            key='toolbar-print'
            className={css(styles.toolbarButton)}
            icon='print'
            title='Print page'
            onClick={window.print}
          />
        </div>
      </NavItem>
    );
  }

  /**
   * Return the button which toggles the display of tags.
   */
  tagsButton() {
    const toolbarButtonStyle = this.state.displayTags ? (
      getToggledButtonStyle(this.props.status)): css(styles.toolbarButton);
    const iconTooltip = this.state.displayTags ? "Hide tags" : "Display tags";

    return (
      <NavItem>
        <div className={css(styles.buttonsBar)}>
          <FontAwesomeIcon
            key='toolbar-tags'
            className={toolbarButtonStyle}
            icon='tags'
            title={iconTooltip}
            onClick={this.toggleTagsDisplay}
          />
        </div>
      </NavItem>
    );
  }

  /**
   * Return the button which toggles the help modal.
   */
  helpButton() {
    return (
      <NavItem>
        <div className={css(styles.buttonsBar)}>
          <FontAwesomeIcon
            key='toolbar-question'
            className={css(styles.toolbarButton)}
            icon='question-circle'
            title='Help'
            onClick={this.toggleHelpOnClick}
          />
        </div>
      </NavItem>
    );
  }

  /**
   * Return the button which links to the documentation.
   */
  documentationButton() {
    return (
      <NavItem>
        <a href='http://testplan.readthedocs.io'
          rel='noopener noreferrer' target='_blank'
          className={css(styles.buttonsBar)}>
          <FontAwesomeIcon
            key='toolbar-document'
            className={css(styles.toolbarButton)}
            icon='book'
            title='Documentation'
          />
        </a>
      </NavItem>
    );
  }

  /**
   * Return the navbar including all buttons.
   */
  navbar() {
    const toolbarStyle = getToolbarStyle(this.props.status);

    return (
      <Navbar light expand="md" className={css(styles.toolbar)}>
        <div className={css(styles.filterBox)}>
          <FilterBox
            width={this.props.filterBoxWidth}
            handleNavFilter={this.props.handleNavFilter}
          />
        </div>
        <Collapse isOpen={this.state.isOpen} navbar className={toolbarStyle}>
          <Nav navbar className='ml-auto'>
            {this.props.extraButtons}
            {this.infoButton()}
            {this.filterButton(toolbarStyle)}
            {this.printButton()}
            {this.tagsButton()}
            {this.helpButton()}
            {this.documentationButton()}
          </Nav>
        </Collapse>
      </Navbar>
    );
  }

  /**
   * Return the help modal.
   */
  helpModal() {
    return (
      <Modal
        isOpen={this.state.helpModal}
        toggle={this.toggleHelpOnClick}
        className='HelpModal'
      >
        <ModalHeader toggle={this.toggleHelpOnClick}>Help</ModalHeader>
        <ModalBody>
          This is filter box help!
        </ModalBody>
        <ModalFooter>
          <Button color="light" onClick={this.toggleHelpOnClick}>
            Close
          </Button>
        </ModalFooter>
      </Modal>
    );
  }

  /**
   * Return the information modal.
   */
  infoModal() {
    return (
      <Modal
        isOpen={this.state.infoModal}
        toggle={this.toggleInfoOnClick}
        size='lg'
        className='infoModal'
      >
        <ModalHeader toggle={this.toggleInfoOnClick}>
          Information
        </ModalHeader>
        <ModalBody>
          {getInfoTable(this.props.report)}
        </ModalBody>
        <ModalFooter>
          <Button color="light" onClick={this.toggleInfoOnClick}>
            Close
          </Button>
        </ModalFooter>
      </Modal>
    );
  }

  /**
   * Render the toolbar component.
   */
  render() {
    return (
      <div>
        {this.navbar()}
        {this.helpModal()}
        {this.infoModal()}
      </div>
    );
  }
}

/**
 * Get the current toolbar style based on the testplan status.
 */
const getToolbarStyle = (status) => {
  switch (STATUS_CATEGORY[status]) {
    case 'passed':
        return css(styles.toolbar, styles.toolbarPassed);
    case 'failed':
    case 'error':
        return css(styles.toolbar, styles.toolbarFailed);
    case 'unstable':
        return css(styles.toolbar, styles.toolbarUnstable);
    default:
        return css(styles.toolbar, styles.toolbarUnknown);
  }
};

/**
 * Get the current toggled toolbar button style in based on the testplan status.
 */
const getToggledButtonStyle = (status) => {
  switch (STATUS_CATEGORY[status]) {
    case 'passed':
        return css(styles.toolbarButton, styles.toolbarButtonToggledPassed);
    case 'failed':
    case 'error':
        return css(styles.toolbarButton, styles.toolbarButtonToggledFailed);
    case 'unstable':
        return css(styles.toolbarButton, styles.toolbarButtonToggledUnstable);
    default:
        return css(styles.toolbarButton, styles.toolbarButtonToggledUnknown);
  }
};

/**
 * Get the metadata from the report and render it as a table.
 */
const getInfoTable = (report) => {
  if (!report || !report.information) {
    return "No information to display.";
  }
  const infoList = report.information.map((item, i) => {
    return (
      <tr key={i}>
        <td className={css(styles.infoTableKey)}>{item[0]}</td>
        <td className={css(styles.infoTableValue)}>{item[1]}</td>
      </tr>
    );
  });
  if (report.timer && report.timer.run) {
    if (report.timer.run.start) {
      infoList.push(
        <tr key='start'>
          <td>start</td>
          <td>{report.timer.run.start}</td>
        </tr>
      );
    }
    if (report.timer.run.end) {
      infoList.push(
        <tr key='end'>
          <td>end</td>
          <td>{report.timer.run.end}</td>
        </tr>
      );
    }
  }
  return (
    <Table bordered responsive className={css(styles.infoTable)}>
      <tbody>
        {infoList}
      </tbody>
    </Table>
  );
};

Toolbar.propTypes = {
  /** Testplan report's status */
  status: PropTypes.oneOf(STATUS),
  /** Report object to display information */
  report: PropTypes.object,
  /** Additional buttons added to toolbar */
  extraButtons: PropTypes.array,
  /** Function to handle filter changing in the Filter box */
  updateFilterFunc: PropTypes.func,
  /** Function to handle toggle of displaying empty entries in the navbar */
  updateEmptyDisplayFunc: PropTypes.func,
  /** Function to handle toggle of displaying tags in the navbar */
  updateTagsDisplayFunc: PropTypes.func,
  /** Function to handle expressions entered into the Filter box */
  handleNavFilter: PropTypes.func,
};

export default Toolbar;
export {getToggledButtonStyle};
