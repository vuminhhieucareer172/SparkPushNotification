package com.yourway.alert.web.rest;

import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.Matchers.hasItem;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import com.yourway.alert.IntegrationTest;
import com.yourway.alert.domain.Query;
import com.yourway.alert.domain.enumeration.EducationLevel;
import com.yourway.alert.domain.enumeration.TypeQuery;
import com.yourway.alert.repository.QueryRepository;
import java.time.Duration;
import java.util.List;
import java.util.Random;
import java.util.concurrent.atomic.AtomicLong;
import javax.persistence.EntityManager;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.Base64Utils;

/**
 * Integration tests for the {@link QueryResource} REST controller.
 */
@IntegrationTest
@AutoConfigureMockMvc
@WithMockUser
class QueryResourceIT {

    private static final Integer DEFAULT_USER_ID = 1;
    private static final Integer UPDATED_USER_ID = 2;

    private static final String DEFAULT_NAME = "AAAAAAAAAA";
    private static final String UPDATED_NAME = "BBBBBBBBBB";

    private static final TypeQuery DEFAULT_TYPE_QUERY = TypeQuery.NORMAL;
    private static final TypeQuery UPDATED_TYPE_QUERY = TypeQuery.QUERY;

    private static final String DEFAULT_COMPANY_ADDRESS = "AAAAAAAAAA";
    private static final String UPDATED_COMPANY_ADDRESS = "BBBBBBBBBB";

    private static final String DEFAULT_JOB_ROLE = "AAAAAAAAAA";
    private static final String UPDATED_JOB_ROLE = "BBBBBBBBBB";

    private static final Integer DEFAULT_AGE = 1;
    private static final Integer UPDATED_AGE = 2;

    private static final Long DEFAULT_SALARY = 1L;
    private static final Long UPDATED_SALARY = 2L;

    private static final Float DEFAULT_YEAR_EXPERIENCES = 1F;
    private static final Float UPDATED_YEAR_EXPERIENCES = 2F;

    private static final EducationLevel DEFAULT_EDUCATION_LEVEL = EducationLevel.POSTGRADUATE;
    private static final EducationLevel UPDATED_EDUCATION_LEVEL = EducationLevel.UNIVERSITY;

    private static final String DEFAULT_JOB_ATTRIBUTE = "AAAAAAAAAA";
    private static final String UPDATED_JOB_ATTRIBUTE = "BBBBBBBBBB";

    private static final String DEFAULT_CONTACT = "AAAAAAAAAA";
    private static final String UPDATED_CONTACT = "BBBBBBBBBB";

    private static final String DEFAULT_GROUP_BY = "AAAAAAAAAA";
    private static final String UPDATED_GROUP_BY = "BBBBBBBBBB";

    private static final Duration DEFAULT_SLIDE_WINDOW = Duration.ofHours(6);
    private static final Duration UPDATED_SLIDE_WINDOW = Duration.ofHours(12);

    private static final String ENTITY_API_URL = "/api/queries";
    private static final String ENTITY_API_URL_ID = ENTITY_API_URL + "/{id}";

    private static Random random = new Random();
    private static AtomicLong count = new AtomicLong(random.nextInt() + (2 * Integer.MAX_VALUE));

    @Autowired
    private QueryRepository queryRepository;

    @Autowired
    private EntityManager em;

    @Autowired
    private MockMvc restQueryMockMvc;

    private Query query;

    /**
     * Create an entity for this test.
     *
     * This is a static method, as tests for other entities might also need it,
     * if they test an entity which requires the current entity.
     */
    public static Query createEntity(EntityManager em) {
        Query query = new Query()
            .userId(DEFAULT_USER_ID)
            .name(DEFAULT_NAME)
            .typeQuery(DEFAULT_TYPE_QUERY)
            .companyAddress(DEFAULT_COMPANY_ADDRESS)
            .jobRole(DEFAULT_JOB_ROLE)
            .age(DEFAULT_AGE)
            .salary(DEFAULT_SALARY)
            .yearExperiences(DEFAULT_YEAR_EXPERIENCES)
            .educationLevel(DEFAULT_EDUCATION_LEVEL)
            .jobAttribute(DEFAULT_JOB_ATTRIBUTE)
            .contact(DEFAULT_CONTACT)
            .groupBy(DEFAULT_GROUP_BY)
            .slideWindow(DEFAULT_SLIDE_WINDOW);
        return query;
    }

    /**
     * Create an updated entity for this test.
     *
     * This is a static method, as tests for other entities might also need it,
     * if they test an entity which requires the current entity.
     */
    public static Query createUpdatedEntity(EntityManager em) {
        Query query = new Query()
            .userId(UPDATED_USER_ID)
            .name(UPDATED_NAME)
            .typeQuery(UPDATED_TYPE_QUERY)
            .companyAddress(UPDATED_COMPANY_ADDRESS)
            .jobRole(UPDATED_JOB_ROLE)
            .age(UPDATED_AGE)
            .salary(UPDATED_SALARY)
            .yearExperiences(UPDATED_YEAR_EXPERIENCES)
            .educationLevel(UPDATED_EDUCATION_LEVEL)
            .jobAttribute(UPDATED_JOB_ATTRIBUTE)
            .contact(UPDATED_CONTACT)
            .groupBy(UPDATED_GROUP_BY)
            .slideWindow(UPDATED_SLIDE_WINDOW);
        return query;
    }

    @BeforeEach
    public void initTest() {
        query = createEntity(em);
    }

    @Test
    @Transactional
    void createQuery() throws Exception {
        int databaseSizeBeforeCreate = queryRepository.findAll().size();
        // Create the Query
        restQueryMockMvc
            .perform(post(ENTITY_API_URL).contentType(MediaType.APPLICATION_JSON).content(TestUtil.convertObjectToJsonBytes(query)))
            .andExpect(status().isCreated());

        // Validate the Query in the database
        List<Query> queryList = queryRepository.findAll();
        assertThat(queryList).hasSize(databaseSizeBeforeCreate + 1);
        Query testQuery = queryList.get(queryList.size() - 1);
        assertThat(testQuery.getUserId()).isEqualTo(DEFAULT_USER_ID);
        assertThat(testQuery.getName()).isEqualTo(DEFAULT_NAME);
        assertThat(testQuery.getTypeQuery()).isEqualTo(DEFAULT_TYPE_QUERY);
        assertThat(testQuery.getCompanyAddress()).isEqualTo(DEFAULT_COMPANY_ADDRESS);
        assertThat(testQuery.getJobRole()).isEqualTo(DEFAULT_JOB_ROLE);
        assertThat(testQuery.getAge()).isEqualTo(DEFAULT_AGE);
        assertThat(testQuery.getSalary()).isEqualTo(DEFAULT_SALARY);
        assertThat(testQuery.getYearExperiences()).isEqualTo(DEFAULT_YEAR_EXPERIENCES);
        assertThat(testQuery.getEducationLevel()).isEqualTo(DEFAULT_EDUCATION_LEVEL);
        assertThat(testQuery.getJobAttribute()).isEqualTo(DEFAULT_JOB_ATTRIBUTE);
        assertThat(testQuery.getContact()).isEqualTo(DEFAULT_CONTACT);
        assertThat(testQuery.getGroupBy()).isEqualTo(DEFAULT_GROUP_BY);
        assertThat(testQuery.getSlideWindow()).isEqualTo(DEFAULT_SLIDE_WINDOW);
    }

    @Test
    @Transactional
    void createQueryWithExistingId() throws Exception {
        // Create the Query with an existing ID
        query.setId(1L);

        int databaseSizeBeforeCreate = queryRepository.findAll().size();

        // An entity with an existing ID cannot be created, so this API call must fail
        restQueryMockMvc
            .perform(post(ENTITY_API_URL).contentType(MediaType.APPLICATION_JSON).content(TestUtil.convertObjectToJsonBytes(query)))
            .andExpect(status().isBadRequest());

        // Validate the Query in the database
        List<Query> queryList = queryRepository.findAll();
        assertThat(queryList).hasSize(databaseSizeBeforeCreate);
    }

    @Test
    @Transactional
    void getAllQueries() throws Exception {
        // Initialize the database
        queryRepository.saveAndFlush(query);

        // Get all the queryList
        restQueryMockMvc
            .perform(get(ENTITY_API_URL + "?sort=id,desc"))
            .andExpect(status().isOk())
            .andExpect(content().contentType(MediaType.APPLICATION_JSON_VALUE))
            .andExpect(jsonPath("$.[*].id").value(hasItem(query.getId().intValue())))
            .andExpect(jsonPath("$.[*].userId").value(hasItem(DEFAULT_USER_ID)))
            .andExpect(jsonPath("$.[*].name").value(hasItem(DEFAULT_NAME)))
            .andExpect(jsonPath("$.[*].typeQuery").value(hasItem(DEFAULT_TYPE_QUERY.toString())))
            .andExpect(jsonPath("$.[*].companyAddress").value(hasItem(DEFAULT_COMPANY_ADDRESS)))
            .andExpect(jsonPath("$.[*].jobRole").value(hasItem(DEFAULT_JOB_ROLE)))
            .andExpect(jsonPath("$.[*].age").value(hasItem(DEFAULT_AGE)))
            .andExpect(jsonPath("$.[*].salary").value(hasItem(DEFAULT_SALARY.intValue())))
            .andExpect(jsonPath("$.[*].yearExperiences").value(hasItem(DEFAULT_YEAR_EXPERIENCES.doubleValue())))
            .andExpect(jsonPath("$.[*].educationLevel").value(hasItem(DEFAULT_EDUCATION_LEVEL.toString())))
            .andExpect(jsonPath("$.[*].jobAttribute").value(hasItem(DEFAULT_JOB_ATTRIBUTE)))
            .andExpect(jsonPath("$.[*].contact").value(hasItem(DEFAULT_CONTACT.toString())))
            .andExpect(jsonPath("$.[*].groupBy").value(hasItem(DEFAULT_GROUP_BY)))
            .andExpect(jsonPath("$.[*].slideWindow").value(hasItem(DEFAULT_SLIDE_WINDOW.toString())));
    }

    @Test
    @Transactional
    void getQuery() throws Exception {
        // Initialize the database
        queryRepository.saveAndFlush(query);

        // Get the query
        restQueryMockMvc
            .perform(get(ENTITY_API_URL_ID, query.getId()))
            .andExpect(status().isOk())
            .andExpect(content().contentType(MediaType.APPLICATION_JSON_VALUE))
            .andExpect(jsonPath("$.id").value(query.getId().intValue()))
            .andExpect(jsonPath("$.userId").value(DEFAULT_USER_ID))
            .andExpect(jsonPath("$.name").value(DEFAULT_NAME))
            .andExpect(jsonPath("$.typeQuery").value(DEFAULT_TYPE_QUERY.toString()))
            .andExpect(jsonPath("$.companyAddress").value(DEFAULT_COMPANY_ADDRESS))
            .andExpect(jsonPath("$.jobRole").value(DEFAULT_JOB_ROLE))
            .andExpect(jsonPath("$.age").value(DEFAULT_AGE))
            .andExpect(jsonPath("$.salary").value(DEFAULT_SALARY.intValue()))
            .andExpect(jsonPath("$.yearExperiences").value(DEFAULT_YEAR_EXPERIENCES.doubleValue()))
            .andExpect(jsonPath("$.educationLevel").value(DEFAULT_EDUCATION_LEVEL.toString()))
            .andExpect(jsonPath("$.jobAttribute").value(DEFAULT_JOB_ATTRIBUTE))
            .andExpect(jsonPath("$.contact").value(DEFAULT_CONTACT.toString()))
            .andExpect(jsonPath("$.groupBy").value(DEFAULT_GROUP_BY))
            .andExpect(jsonPath("$.slideWindow").value(DEFAULT_SLIDE_WINDOW.toString()));
    }

    @Test
    @Transactional
    void getNonExistingQuery() throws Exception {
        // Get the query
        restQueryMockMvc.perform(get(ENTITY_API_URL_ID, Long.MAX_VALUE)).andExpect(status().isNotFound());
    }

    @Test
    @Transactional
    void putNewQuery() throws Exception {
        // Initialize the database
        queryRepository.saveAndFlush(query);

        int databaseSizeBeforeUpdate = queryRepository.findAll().size();

        // Update the query
        Query updatedQuery = queryRepository.findById(query.getId()).get();
        // Disconnect from session so that the updates on updatedQuery are not directly saved in db
        em.detach(updatedQuery);
        updatedQuery
            .userId(UPDATED_USER_ID)
            .name(UPDATED_NAME)
            .typeQuery(UPDATED_TYPE_QUERY)
            .companyAddress(UPDATED_COMPANY_ADDRESS)
            .jobRole(UPDATED_JOB_ROLE)
            .age(UPDATED_AGE)
            .salary(UPDATED_SALARY)
            .yearExperiences(UPDATED_YEAR_EXPERIENCES)
            .educationLevel(UPDATED_EDUCATION_LEVEL)
            .jobAttribute(UPDATED_JOB_ATTRIBUTE)
            .contact(UPDATED_CONTACT)
            .groupBy(UPDATED_GROUP_BY)
            .slideWindow(UPDATED_SLIDE_WINDOW);

        restQueryMockMvc
            .perform(
                put(ENTITY_API_URL_ID, updatedQuery.getId())
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(TestUtil.convertObjectToJsonBytes(updatedQuery))
            )
            .andExpect(status().isOk());

        // Validate the Query in the database
        List<Query> queryList = queryRepository.findAll();
        assertThat(queryList).hasSize(databaseSizeBeforeUpdate);
        Query testQuery = queryList.get(queryList.size() - 1);
        assertThat(testQuery.getUserId()).isEqualTo(UPDATED_USER_ID);
        assertThat(testQuery.getName()).isEqualTo(UPDATED_NAME);
        assertThat(testQuery.getTypeQuery()).isEqualTo(UPDATED_TYPE_QUERY);
        assertThat(testQuery.getCompanyAddress()).isEqualTo(UPDATED_COMPANY_ADDRESS);
        assertThat(testQuery.getJobRole()).isEqualTo(UPDATED_JOB_ROLE);
        assertThat(testQuery.getAge()).isEqualTo(UPDATED_AGE);
        assertThat(testQuery.getSalary()).isEqualTo(UPDATED_SALARY);
        assertThat(testQuery.getYearExperiences()).isEqualTo(UPDATED_YEAR_EXPERIENCES);
        assertThat(testQuery.getEducationLevel()).isEqualTo(UPDATED_EDUCATION_LEVEL);
        assertThat(testQuery.getJobAttribute()).isEqualTo(UPDATED_JOB_ATTRIBUTE);
        assertThat(testQuery.getContact()).isEqualTo(UPDATED_CONTACT);
        assertThat(testQuery.getGroupBy()).isEqualTo(UPDATED_GROUP_BY);
        assertThat(testQuery.getSlideWindow()).isEqualTo(UPDATED_SLIDE_WINDOW);
    }

    @Test
    @Transactional
    void putNonExistingQuery() throws Exception {
        int databaseSizeBeforeUpdate = queryRepository.findAll().size();
        query.setId(count.incrementAndGet());

        // If the entity doesn't have an ID, it will throw BadRequestAlertException
        restQueryMockMvc
            .perform(
                put(ENTITY_API_URL_ID, query.getId())
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(TestUtil.convertObjectToJsonBytes(query))
            )
            .andExpect(status().isBadRequest());

        // Validate the Query in the database
        List<Query> queryList = queryRepository.findAll();
        assertThat(queryList).hasSize(databaseSizeBeforeUpdate);
    }

    @Test
    @Transactional
    void putWithIdMismatchQuery() throws Exception {
        int databaseSizeBeforeUpdate = queryRepository.findAll().size();
        query.setId(count.incrementAndGet());

        // If url ID doesn't match entity ID, it will throw BadRequestAlertException
        restQueryMockMvc
            .perform(
                put(ENTITY_API_URL_ID, count.incrementAndGet())
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(TestUtil.convertObjectToJsonBytes(query))
            )
            .andExpect(status().isBadRequest());

        // Validate the Query in the database
        List<Query> queryList = queryRepository.findAll();
        assertThat(queryList).hasSize(databaseSizeBeforeUpdate);
    }

    @Test
    @Transactional
    void putWithMissingIdPathParamQuery() throws Exception {
        int databaseSizeBeforeUpdate = queryRepository.findAll().size();
        query.setId(count.incrementAndGet());

        // If url ID doesn't match entity ID, it will throw BadRequestAlertException
        restQueryMockMvc
            .perform(put(ENTITY_API_URL).contentType(MediaType.APPLICATION_JSON).content(TestUtil.convertObjectToJsonBytes(query)))
            .andExpect(status().isMethodNotAllowed());

        // Validate the Query in the database
        List<Query> queryList = queryRepository.findAll();
        assertThat(queryList).hasSize(databaseSizeBeforeUpdate);
    }

    @Test
    @Transactional
    void partialUpdateQueryWithPatch() throws Exception {
        // Initialize the database
        queryRepository.saveAndFlush(query);

        int databaseSizeBeforeUpdate = queryRepository.findAll().size();

        // Update the query using partial update
        Query partialUpdatedQuery = new Query();
        partialUpdatedQuery.setId(query.getId());

        partialUpdatedQuery.jobRole(UPDATED_JOB_ROLE).salary(UPDATED_SALARY).groupBy(UPDATED_GROUP_BY);

        restQueryMockMvc
            .perform(
                patch(ENTITY_API_URL_ID, partialUpdatedQuery.getId())
                    .contentType("application/merge-patch+json")
                    .content(TestUtil.convertObjectToJsonBytes(partialUpdatedQuery))
            )
            .andExpect(status().isOk());

        // Validate the Query in the database
        List<Query> queryList = queryRepository.findAll();
        assertThat(queryList).hasSize(databaseSizeBeforeUpdate);
        Query testQuery = queryList.get(queryList.size() - 1);
        assertThat(testQuery.getUserId()).isEqualTo(DEFAULT_USER_ID);
        assertThat(testQuery.getName()).isEqualTo(DEFAULT_NAME);
        assertThat(testQuery.getTypeQuery()).isEqualTo(DEFAULT_TYPE_QUERY);
        assertThat(testQuery.getCompanyAddress()).isEqualTo(DEFAULT_COMPANY_ADDRESS);
        assertThat(testQuery.getJobRole()).isEqualTo(UPDATED_JOB_ROLE);
        assertThat(testQuery.getAge()).isEqualTo(DEFAULT_AGE);
        assertThat(testQuery.getSalary()).isEqualTo(UPDATED_SALARY);
        assertThat(testQuery.getYearExperiences()).isEqualTo(DEFAULT_YEAR_EXPERIENCES);
        assertThat(testQuery.getEducationLevel()).isEqualTo(DEFAULT_EDUCATION_LEVEL);
        assertThat(testQuery.getJobAttribute()).isEqualTo(DEFAULT_JOB_ATTRIBUTE);
        assertThat(testQuery.getContact()).isEqualTo(DEFAULT_CONTACT);
        assertThat(testQuery.getGroupBy()).isEqualTo(UPDATED_GROUP_BY);
        assertThat(testQuery.getSlideWindow()).isEqualTo(DEFAULT_SLIDE_WINDOW);
    }

    @Test
    @Transactional
    void fullUpdateQueryWithPatch() throws Exception {
        // Initialize the database
        queryRepository.saveAndFlush(query);

        int databaseSizeBeforeUpdate = queryRepository.findAll().size();

        // Update the query using partial update
        Query partialUpdatedQuery = new Query();
        partialUpdatedQuery.setId(query.getId());

        partialUpdatedQuery
            .userId(UPDATED_USER_ID)
            .name(UPDATED_NAME)
            .typeQuery(UPDATED_TYPE_QUERY)
            .companyAddress(UPDATED_COMPANY_ADDRESS)
            .jobRole(UPDATED_JOB_ROLE)
            .age(UPDATED_AGE)
            .salary(UPDATED_SALARY)
            .yearExperiences(UPDATED_YEAR_EXPERIENCES)
            .educationLevel(UPDATED_EDUCATION_LEVEL)
            .jobAttribute(UPDATED_JOB_ATTRIBUTE)
            .contact(UPDATED_CONTACT)
            .groupBy(UPDATED_GROUP_BY)
            .slideWindow(UPDATED_SLIDE_WINDOW);

        restQueryMockMvc
            .perform(
                patch(ENTITY_API_URL_ID, partialUpdatedQuery.getId())
                    .contentType("application/merge-patch+json")
                    .content(TestUtil.convertObjectToJsonBytes(partialUpdatedQuery))
            )
            .andExpect(status().isOk());

        // Validate the Query in the database
        List<Query> queryList = queryRepository.findAll();
        assertThat(queryList).hasSize(databaseSizeBeforeUpdate);
        Query testQuery = queryList.get(queryList.size() - 1);
        assertThat(testQuery.getUserId()).isEqualTo(UPDATED_USER_ID);
        assertThat(testQuery.getName()).isEqualTo(UPDATED_NAME);
        assertThat(testQuery.getTypeQuery()).isEqualTo(UPDATED_TYPE_QUERY);
        assertThat(testQuery.getCompanyAddress()).isEqualTo(UPDATED_COMPANY_ADDRESS);
        assertThat(testQuery.getJobRole()).isEqualTo(UPDATED_JOB_ROLE);
        assertThat(testQuery.getAge()).isEqualTo(UPDATED_AGE);
        assertThat(testQuery.getSalary()).isEqualTo(UPDATED_SALARY);
        assertThat(testQuery.getYearExperiences()).isEqualTo(UPDATED_YEAR_EXPERIENCES);
        assertThat(testQuery.getEducationLevel()).isEqualTo(UPDATED_EDUCATION_LEVEL);
        assertThat(testQuery.getJobAttribute()).isEqualTo(UPDATED_JOB_ATTRIBUTE);
        assertThat(testQuery.getContact()).isEqualTo(UPDATED_CONTACT);
        assertThat(testQuery.getGroupBy()).isEqualTo(UPDATED_GROUP_BY);
        assertThat(testQuery.getSlideWindow()).isEqualTo(UPDATED_SLIDE_WINDOW);
    }

    @Test
    @Transactional
    void patchNonExistingQuery() throws Exception {
        int databaseSizeBeforeUpdate = queryRepository.findAll().size();
        query.setId(count.incrementAndGet());

        // If the entity doesn't have an ID, it will throw BadRequestAlertException
        restQueryMockMvc
            .perform(
                patch(ENTITY_API_URL_ID, query.getId())
                    .contentType("application/merge-patch+json")
                    .content(TestUtil.convertObjectToJsonBytes(query))
            )
            .andExpect(status().isBadRequest());

        // Validate the Query in the database
        List<Query> queryList = queryRepository.findAll();
        assertThat(queryList).hasSize(databaseSizeBeforeUpdate);
    }

    @Test
    @Transactional
    void patchWithIdMismatchQuery() throws Exception {
        int databaseSizeBeforeUpdate = queryRepository.findAll().size();
        query.setId(count.incrementAndGet());

        // If url ID doesn't match entity ID, it will throw BadRequestAlertException
        restQueryMockMvc
            .perform(
                patch(ENTITY_API_URL_ID, count.incrementAndGet())
                    .contentType("application/merge-patch+json")
                    .content(TestUtil.convertObjectToJsonBytes(query))
            )
            .andExpect(status().isBadRequest());

        // Validate the Query in the database
        List<Query> queryList = queryRepository.findAll();
        assertThat(queryList).hasSize(databaseSizeBeforeUpdate);
    }

    @Test
    @Transactional
    void patchWithMissingIdPathParamQuery() throws Exception {
        int databaseSizeBeforeUpdate = queryRepository.findAll().size();
        query.setId(count.incrementAndGet());

        // If url ID doesn't match entity ID, it will throw BadRequestAlertException
        restQueryMockMvc
            .perform(patch(ENTITY_API_URL).contentType("application/merge-patch+json").content(TestUtil.convertObjectToJsonBytes(query)))
            .andExpect(status().isMethodNotAllowed());

        // Validate the Query in the database
        List<Query> queryList = queryRepository.findAll();
        assertThat(queryList).hasSize(databaseSizeBeforeUpdate);
    }

    @Test
    @Transactional
    void deleteQuery() throws Exception {
        // Initialize the database
        queryRepository.saveAndFlush(query);

        int databaseSizeBeforeDelete = queryRepository.findAll().size();

        // Delete the query
        restQueryMockMvc
            .perform(delete(ENTITY_API_URL_ID, query.getId()).accept(MediaType.APPLICATION_JSON))
            .andExpect(status().isNoContent());

        // Validate the database contains one less item
        List<Query> queryList = queryRepository.findAll();
        assertThat(queryList).hasSize(databaseSizeBeforeDelete - 1);
    }
}
